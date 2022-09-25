param    # 스크립트를 실행하려면 경로를 입력해야한다
(
    [String]
    [Parameter(Mandatory)]
    $Path,                          # 실행하려는 txt 파일
    [String]
    [Parameter(Mandatory)]
    $ResultPath                # 결과를 저장할 txt 파일 
)      

function Run-PsParser
{ 
  param
  (
    [String]
    [Parameter(Mandatory,ValueFromPipeline)]
    $Path
  )
  begin { 
     $errors = $null
  }
  process {
    # 에러 저장하기 위한 변수
    $errors = $null
    # 해당 파일의 내용 가져오기
    $code = Get-Content -Path $Path -Raw -Encoding Default
    
    # 리턴값: 파일 이름, 경로, 토큰, 에러
    [PSCustomObject]@{
      Name = Split-Path -Path $Path -Leaf  # 경로에서 이름부분만 가져오기
      Tokens = [Management.Automation.PSParser]::Tokenize($code, [ref]$errors)  # [ref]$errors - 참조변수
      Errors = $errors | Select-Object -ExpandProperty Token -Property Message   #에러 메세지와 에러 토큰 객체 
    }  
  }
}

# txt파일 읽고 txt파일에 결과 저장하는
function Test-parser {
    param
  (
    [String]
    [Parameter(Mandatory)]
    $Path,
    [String]
    [Parameter(Mandatory)]
    $ResultPath
  )
    #경로에서 txt파일 찾고 psparser진행 그리고 뽑아낸 값을 새로운 txt파일에 저장
    Get-ChildItem -Path $Path -Include *.txt -File |
    Run-PsParser |
    Foreach-Object {
       $result = $null
       foreach ($token in $_.Tokens) {
            if (($token.Type -eq 'Command') -or ($token.Type -eq 'CommandArgument')) {
		$result += $token.content 
                 $result += " " 
            }
            if (($token.Type -eq 'Keyword') -or ($token.Type -eq 'CommandParameter') -or ($token.Type -eq 'Variable') ) {
		#Add-Content $file -Value  $token.content
                 $result += $token.content 
                 $result += " " 
            }
       }  
       $result | Set-Content $ResultPath   

    }  
    
}

Test-parser -Path $Path $ResultPath #입력한 경로로 psparser실행하기