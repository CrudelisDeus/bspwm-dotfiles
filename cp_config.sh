rm -R ./.config
cp -R ~/.config .config

rm -R ./bash
mkdir ./bash
cp ~/.bash_logout ./bash
cp ~/.bash_profile ./bash
cp ~/.bashrc ./bash
cp ~/.xinitrc ./bash
