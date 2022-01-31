VER = $(shell python3 -c "from main import __version__; print(__version__)")
FLAGS = --onefile \
		--hidden-import=PIL._tkinter_finder \
		--clean \
		--distpath=./ \
		--name=CApy_v$(VER) \
		--icon=img/capy.ico

all: compile clean

compile:
	pyinstaller main.py $(FLAGS)

clean:
	rm -r *.spec build/ __pycache__/
