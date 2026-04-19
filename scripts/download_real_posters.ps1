$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
$posterDir = Join-Path $projectRoot "assets\\posters"
New-Item -ItemType Directory -Path $posterDir -Force | Out-Null

$movieJson = & python -c "from database import MOVIE_CATALOG; import json; print(json.dumps([{'title': m['title'], 'year': m['year']} for m in MOVIE_CATALOG]))"
$movies = $movieJson | ConvertFrom-Json
$headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

function Get-Slug {
    param([string]$Text)

    $slug = $Text.ToLowerInvariant() -replace "[^a-z0-9]+", "-"
    return $slug.Trim("-")
}

function Get-FirstMatch {
    param(
        [string]$Text,
        [string]$Pattern
    )

    $match = [System.Text.RegularExpressions.Regex]::Match(
        $Text,
        $Pattern,
        [System.Text.RegularExpressions.RegexOptions]::IgnoreCase
    )

    if ($match.Success) {
        return $match.Groups[1].Value
    }

    return $null
}

function Get-MoviePageUrl {
    param(
        [string]$Title,
        [int]$Year
    )

    $query = [System.Uri]::EscapeDataString("$Title y:$Year")
    $searchUrl = "https://www.themoviedb.org/search/movie?query=$query"
    $response = Invoke-WebRequest -UseBasicParsing -Headers $headers -Uri $searchUrl

    $relativePath = Get-FirstMatch -Text $response.Content -Pattern 'href="(/movie/\d+[^"]*)"'
    if (-not $relativePath) {
        throw "No TMDB match found for $Title ($Year)."
    }

    return "https://www.themoviedb.org$relativePath"
}

function Get-PosterUrl {
    param([string]$MoviePageUrl)

    $posterPageUrl = "$MoviePageUrl/images/posters?language=en-US"
    $response = Invoke-WebRequest -UseBasicParsing -Headers $headers -Uri $posterPageUrl

    $posterUrl = Get-FirstMatch -Text $response.Content -Pattern 'href="(https://image\.tmdb\.org/t/p/original/[^"]+)"'
    if ($posterUrl) {
        return $posterUrl
    }

    $posterUrl = Get-FirstMatch -Text $response.Content -Pattern 'href="(https://media\.themoviedb\.org/t/p/original/[^"]+)"'
    if ($posterUrl) {
        return $posterUrl
    }

    $posterPath = Get-FirstMatch -Text $response.Content -Pattern 'https://(?:image|media)\.tmdb\.org/t/p/(?:w\d+[^" ]*|original)(/[^" ]+\.(?:jpg|jpeg|png))'
    if ($posterPath) {
        return "https://image.tmdb.org/t/p/original$posterPath"
    }

    throw "No poster image found for $MoviePageUrl."
}

function Convert-ToPng {
    param(
        [string]$SourcePath,
        [string]$DestinationPath
    )

    $image = [System.Drawing.Image]::FromFile($SourcePath)
    $bitmap = New-Object System.Drawing.Bitmap($image.Width, $image.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)

    try {
        $graphics.DrawImage($image, 0, 0, $image.Width, $image.Height)
        $bitmap.Save($DestinationPath, [System.Drawing.Imaging.ImageFormat]::Png)
    }
    finally {
        $graphics.Dispose()
        $bitmap.Dispose()
        $image.Dispose()
    }
}

$downloaded = New-Object System.Collections.Generic.List[string]

foreach ($movie in $movies) {
    $slug = Get-Slug $movie.title
    $outputPath = Join-Path $posterDir "$slug.png"
    $tempPath = Join-Path $env:TEMP "$slug-source"

    Write-Output "Fetching poster for $($movie.title) ($($movie.year))..."

    $moviePageUrl = Get-MoviePageUrl -Title $movie.title -Year $movie.year
    $posterUrl = Get-PosterUrl -MoviePageUrl $moviePageUrl

    Invoke-WebRequest -UseBasicParsing -Headers $headers -Uri $posterUrl -OutFile $tempPath
    Convert-ToPng -SourcePath $tempPath -DestinationPath $outputPath
    Remove-Item -LiteralPath $tempPath -Force

    $downloaded.Add("$($movie.title) -> $posterUrl") | Out-Null
}

Write-Output ""
Write-Output "Downloaded $($downloaded.Count) poster images into $posterDir"
