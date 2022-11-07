### 1. 프로젝트 소개

* (AI 보안) NLP 기반 PowerShell 악성 스크립트 탐지 툴 개발<br>
* 난독화된 스크립트 분석을 위한 비난독화 모듈과 머신 러닝 기법을 활용한 악성 스크립트 분류 모듈을 개발한다.

### 2. 팀소개

김서영, ksy654333@gmail.com, 전처리, 악성 스크립트 분류 모델 구현

박지연, oy5325@naver.com, 악성 스크립트 분류 모델 구현, 모델 학습 및 평가

최연재, duswo0624@naver.com, 비난독화 모듈 개발, GUI 시각화 도구 개발

### 3. 시스템 구성도

![시스템 구성도](https://user-images.githubusercontent.com/61836238/195824883-f5cbfb10-4058-4f99-966f-db0be5dcbcb7.PNG)
1. 비난독화는 BASE64와 16진수를 이용한 방식으로 진행된다.
2. PowerShell 스크립트에서 필요한 명령어만을 뽑아내는 전처리 과정을 거친다.
3. AdaBoost, GBM, XGBoost 세가지를 앙상블한 모델을 사용하여 악성 스크립트를 탐지한다.

### 4. 소개 및 시연 영상
[![47조 NLP 기반 Powershell 악성 스크립트 탐지 툴](http://img.youtube.com/vi/BcZA0i-ySRo/0.jpg)](https://www.youtube.com/watch?v=BcZA0i-ySRo)    

### 5. 설치 및 사용법

본 프로젝트는 Python3 버전에서 개발되었습니다.<br>
아래의 코드를 이용하여 배치파일을 생성 후 이용하실 수 있습니다.
```
$ pyinstaller .\main.spec
```
