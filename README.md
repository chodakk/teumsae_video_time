# Teumsae's Video Time Calculator
![charmander-from-pokemon](https://github.com/user-attachments/assets/ab64618c-f83d-4ef7-b456-cb2abdaa9b04)

## 설치 방법 및 exe 파일 생성 방법
1. 녹색 code 버튼 클릭 후 Download Zip
2. 압축파일 해제 후 에디터(vs code, pycharm 등...)로 실행
3. 터미널에서 `pip install -r requirements.txt` 명령어 실행
4. 터미널에서 `pip show tkfilebrowser` 명령어 실행
5. Location 위치에 있는 path 복사 (예시: `c:\users\Chodakk\desktop\teumsae_video_time\venv\lib\site-packages`)
6. 프로젝트 내 `main.spec` 파일 열기
7. 파일 수정
    ```python
    a.datas += Tree(
        r"{5번에서_복사한_path}\tkfilebrowser",
        "tkfilebrowser"
    )
    
    ### 예시
    a.datas += Tree(
        r"c:\users\chodakk\desktop\teumsae_video_time\venv\lib\site-packages\tkfilebrowser",
        "tkfilebrowser"
    )
    ```
8. 터미널에서 `pyinstaller.exe main.spec` 실행
9. 기다린 후 프로젝트 내 dist 폴더 안에 .exe 파일이 생성!!!
