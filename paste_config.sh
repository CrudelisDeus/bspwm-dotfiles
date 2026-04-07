rm -R ~/.config/*
mkdir ~/.config
cp -R ./config/* ~/.config

rm ~/.bash_logout
rm ~/.bash_profile
rm ~/.bashrc
rm ~/.xinitrc

cp ./home/.* ~/

mkdir ~/.ssh
