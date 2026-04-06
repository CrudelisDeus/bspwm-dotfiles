rm -R ~/.config/*
mkdir ~/.config
cp -R ./config/* ~/.config

rm -R ./home

rm ~/.bash_logout
rm ~/.bash_profile
rm ~/.bashrc
rm ~/.xinitrc

cp ./home/* ~/
