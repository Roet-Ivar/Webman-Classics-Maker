@echo off
if exist EBOOT.BIN goto fix
echo EBOOT.BIN not found...
goto end
:fix
set ContentID=%1
set CID=%ContentID%
FixELF.exe EBOOT.ELF "24 13 BC C5 F6 00 33 00 00 00 36" "24 13 BC C5 F6 00 33 00 00 00 34" /340
echo ContentID=%CID%
scetool.exe -v --sce-type=SELF --compress-data=TRUE --skip-sections=TRUE --key-revision=01 --self-auth-id=1010000001000003 --self-app-version=0001000000000000 --self-add-shdrs=TRUE --self-vendor-id=01000002 --self-type=NPDRM --self-fw-version=0003004000000000 --np-license-type=FREE --np-content-id=%CID% --np-app-type=EXEC --np-real-fname=EBOOT.BIN --encrypt EBOOT.ELF EBOOT.BIN
:end
pause
