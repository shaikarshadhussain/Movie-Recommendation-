$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
$posterDir = Join-Path $projectRoot "assets\\posters"
New-Item -ItemType Directory -Path $posterDir -Force | Out-Null

$movieJson = & python -c "from database import MOVIE_CATALOG; import json; print(json.dumps([{'title': m['title'], 'year': m['year'], 'genre': m['genre'], 'tagline': m['tagline']} for m in MOVIE_CATALOG]))"
$movies = $movieJson | ConvertFrom-Json

$palettes = @(
    @{ Start = "#071B34"; End = "#0E4D77"; Accent = "#1AD0FF"; Soft = "#9FE7FF" },
    @{ Start = "#2A163A"; End = "#6A2F7C"; Accent = "#FF7DD4"; Soft = "#F4C0FF" },
    @{ Start = "#10222E"; End = "#0E5C5F"; Accent = "#52F2C9"; Soft = "#C8FFF1" },
    @{ Start = "#25140F"; End = "#8A3E1E"; Accent = "#FFBB4D"; Soft = "#FFE2A8" },
    @{ Start = "#1B1E31"; End = "#374F9B"; Accent = "#8BB6FF"; Soft = "#DDE8FF" },
    @{ Start = "#22111E"; End = "#833258"; Accent = "#FF8AAC"; Soft = "#FFD0DC" }
)

function Get-Slug {
    param([string]$Text)

    $slug = $Text.ToLowerInvariant() -replace "[^a-z0-9]+", "-"
    return $slug.Trim("-")
}

function New-Color {
    param([string]$Hex)
    return [System.Drawing.ColorTranslator]::FromHtml($Hex)
}

function Split-PosterLines {
    param(
        [System.Drawing.Graphics]$Graphics,
        [string]$Text,
        [System.Drawing.Font]$Font,
        [int]$MaxWidth,
        [int]$MaxLines = 3
    )

    $words = $Text -split "\s+"
    $lines = New-Object System.Collections.Generic.List[string]
    $current = ""

    foreach ($word in $words) {
        $candidate = if ($current) { "$current $word" } else { $word }
        $size = $Graphics.MeasureString($candidate, $Font)
        if ($size.Width -le $MaxWidth -or -not $current) {
            $current = $candidate
        }
        else {
            $lines.Add($current)
            $current = $word
        }
    }

    if ($current) {
        $lines.Add($current)
    }

    if ($lines.Count -gt $MaxLines) {
        $trimmed = $lines[0..($MaxLines - 1)]
        $trimmed[$MaxLines - 1] = $trimmed[$MaxLines - 1].TrimEnd() + "..."
        return ,$trimmed
    }

    return ,$lines.ToArray()
}

foreach ($movie in $movies) {
    $slug = Get-Slug $movie.title
    $palette = $palettes[[Math]::Abs($movie.title.GetHashCode()) % $palettes.Count]
    $outputPath = Join-Path $posterDir "$slug.png"

    $bitmap = New-Object System.Drawing.Bitmap 360, 540
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

    $bounds = New-Object System.Drawing.Rectangle 0, 0, 360, 540
    $gradient = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
        $bounds,
        (New-Color $palette.Start),
        (New-Color $palette.End),
        55.0
    )
    $graphics.FillRectangle($gradient, $bounds)

    $softBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(35, (New-Color $palette.Soft)))
    $accentBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(85, (New-Color $palette.Accent)))
    $textBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(244, 248, 252))
    $mutedBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(203, 219, 235))
    $lineBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(95, (New-Color $palette.Accent)))

    $graphics.FillEllipse($softBrush, -30, -20, 250, 250)
    $graphics.FillEllipse($accentBrush, 160, 300, 250, 220)
    $graphics.FillRectangle($softBrush, 28, 92, 304, 2)
    $graphics.FillRectangle($lineBrush, 28, 438, 304, 6)
    $graphics.FillRectangle($softBrush, 28, 452, 220, 1)

    $brandFont = New-Object System.Drawing.Font("Segoe UI", 13, [System.Drawing.FontStyle]::Bold)
    $titleFont = New-Object System.Drawing.Font("Segoe UI Semibold", 28, [System.Drawing.FontStyle]::Bold)
    $metaFont = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Regular)
    $taglineFont = New-Object System.Drawing.Font("Segoe UI", 13, [System.Drawing.FontStyle]::Regular)

    $graphics.DrawString("MOODSTREAM SELECT", $brandFont, $mutedBrush, 28, 40)

    $titleLines = Split-PosterLines -Graphics $graphics -Text $movie.title.ToUpperInvariant() -Font $titleFont -MaxWidth 300 -MaxLines 4
    $titleY = 125
    foreach ($line in $titleLines) {
        $graphics.DrawString($line, $titleFont, $textBrush, 28, $titleY)
        $titleY += 42
    }

    $graphics.DrawString([string]$movie.year, $metaFont, $mutedBrush, 28, 392)
    $graphics.DrawString([string]$movie.genre.ToUpperInvariant(), $metaFont, $mutedBrush, 88, 392)

    $taglineLines = Split-PosterLines -Graphics $graphics -Text $movie.tagline -Font $taglineFont -MaxWidth 292 -MaxLines 3
    $taglineY = 462
    foreach ($line in $taglineLines) {
        $graphics.DrawString($line, $taglineFont, $textBrush, 28, $taglineY)
        $taglineY += 22
    }

    $bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)

    $brandFont.Dispose()
    $titleFont.Dispose()
    $metaFont.Dispose()
    $taglineFont.Dispose()
    $softBrush.Dispose()
    $accentBrush.Dispose()
    $textBrush.Dispose()
    $mutedBrush.Dispose()
    $lineBrush.Dispose()
    $gradient.Dispose()
    $graphics.Dispose()
    $bitmap.Dispose()
}

Write-Output "Generated $($movies.Count) poster images in $posterDir"
