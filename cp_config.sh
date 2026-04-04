rm -R ./config
mkdir config
cp -R ~/.config/* config

rm -R ./home
mkdir home
cp ~/.bash_logout ./home
cp ~/.bash_profile ./home
cp ~/.bashrc ./home
cp ~/.xinitrc ./home
