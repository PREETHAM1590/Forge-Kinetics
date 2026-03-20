$ErrorActionPreference = 'Stop'
$projectId = '7619164747869714994'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$outDir = Join-Path $root 'pages'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$ids = @(
  '090f8f3e889c46c4ae997d673720ff26',
  '20dd78a9b7a94121a86938edc2d58e39',
  '264d6507dd8f49c0bb8236800b6918e4',
  '270beaba3844447c92df96b62b9d9f15',
  '356a6ef2fc3b4f8ea3fa2e9997386e58',
  '9021fe18ecd2470e98db48d1c2115daf',
  '94015917cda248bab8c12af0ee05dc02',
  'aca53bca9a7442e891c01de4bdb9d7a8',
  'bb70a2afadb1454daca762e76463684e',
  'c730634f9b8d4f30af0d5b5fa3335112',
  'd2fecfa78c534fcc88fbea4bf330179e',
  'd73e6272d79f434daa2608a3e236c652',
  'e40403bf55f2480d8cd28d3eb8b8a38e',
  'dfcb11286a7844658f838a8a156e4819'
)

foreach ($id in $ids) {
  $url = "https://stitch.withgoogle.com/project/$projectId/screen/$id"
  $out = Join-Path $outDir "$id.html"
  Write-Host "Downloading $id ..."
  curl.exe -L "$url" -o "$out"
}

Write-Host "Done. Files written to: $outDir"
