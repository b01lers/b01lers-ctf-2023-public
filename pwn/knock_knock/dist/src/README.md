# Build

install required tools for building

	sudo pacman -S nasm lld
	cargo install cargo-sysroot

set toolchain and build sysroot

	rustup override set nightly
	./run.sh sysroot

if building sysroot fails, you may have to install rust-src

	rustup component add rust-src

compile with script

	./build.sh
