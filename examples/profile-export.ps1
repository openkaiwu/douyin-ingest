param(
    [Parameter(Mandatory = $true)]
    [string]$ProfileUrl,
    [string]$Output = "output\result.json"
)

python -m pip install -e ".[agent]"
douyin-ingest $ProfileUrl --limit 0 --export docx --output $Output
