; NSIS Install Script

Name "road_router Installer"
OutFile "road_router Installer.exe"
InstallDir $DESKTOP\road_router
RequestExecutionLevel user

Page directory
Page instfiles

Section "Install"
  SetOutPath $INSTDIR
  File road_router.exe
  File /r "Input Data"
  FiLE /r "Output Data"
SectionEnd
