
# AirSim 설치 가이드 (Linux) 🛠️

## 시스템 요구사항 🖥️

- **OS**: Ubuntu 18.04 / 20.04
- **Hardware**: 8GB RAM, 100GB+ 디스크 공간, NVIDIA GPU (CUDA 10.0+)

## 설치 과정 🛠️

### 1. 의존성 패키지 설치 📦

```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake git libjpeg-dev libpng-dev libtiff-dev libgl1-mesa-dev libglu1-mesa-dev
```

### 2. Unreal Engine 설치 🎮

```bash
git clone -b 4.25 git@github.com:EpicGames/UnrealEngine.git
cd UnrealEngine
./Setup.sh
./GenerateProjectFiles.sh
make
```

### 2. AirSim 리포지토리 클론 및 빌드🔄

```bash
git clone https://github.com/microsoft/AirSim.git
cd AirSim
./setup.sh
./build.sh
```

### 3. Unreal Engine의 Project(Environments) 설정 ⚙️

1. 'AirSim\Unreal\Environments' 에 아래 폴더(Blocks 4.25) 넣기
https://drive.google.com/file/d/1kYiO4VMl9_guA7wXr0a67oRY4MTWn6TO/view?usp=sharing
2. '/home/<username>/Documents/AirSim'에 아래 파일(setting.json) 넣기
https://drive.google.com/file/d/1cTUbTPKsYL4YiGLAqBk7-O0RWVn7LVbc/view?usp=sharing


### 4. Python library 설치 (가상환경 추천)⚙️

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2023.03-Linux-x86_64.sh -O anaconda.sh
bash anaconda.sh
source ~/.bashrc
conda list
conda update conda

conda create -n car python=3.8
conda activate car
```

```bash
pip install numpy==1.19.5
pip install pandas==1.1.5
pip install typing-extensions==3.7.4
pip install tornado==4.5.3
pip install grpcio==1.32.0
pip install absl-py==0.10
pip install tensorflow==2.4.1
pip install tensorboard==2.4.1
pip install jupyter-client==7.1.2
pip install ipykernel==5.5.6
pip install torch==1.7.1
pip install torchvision==0.8.2
pip install tensorboardX==2.1
pip install protobuf==3.20.3
pip install psutil
pip install PyYAML
pip install wandb==0.16.6
pip install airsim
pip install gym
pip install matplotlib==3.3.4
pip install tqdm
```

### 5. AirSim 실행 🌟

```bash
.UnrealEngine-4.25/Engine/Binaries/Linux/UE4Editor
```
1. 우측 'More' 버튼 클릭
2. 우측 하단 'Browse...' 클릭
3. 3-1에서 추가한 Blocks 4.25 내의 프로젝트 파일을 열기
4. Convert Option이 주어지면 'Convert-In-Place' 선택하기 (선택지가 없으면 좌측 하단의 see more 클릭)
5. 프로젝트가 열리면 하단 에서 'DARL' 더블 클릭
6. 상단 바에서 'Play'버튼 우측에 드롭박스를 열어 'Standalone game' 선택 후 실행


### ※ 차량 위치 변경 방법 🌟
3-2에서 설정한 setting.json의 파일에서 각 차량의 x,y를 변경 후 환경을 재실행
