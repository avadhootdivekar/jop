
export SEP:="\n#######################################################################################################################\n"
export JOP_VER="1.01"


clean:
	echo "Clean"

all : 
	echo "all"

tools : 
	echo "tools"

test :
	echo "test"

build_container :
# Only this recipe runs outside of the container. Rest all will run inside the container. 
# Build  the  container 
	echo "Building build shell."
	docker build -t jop_builder:${JOP_VER} ./ ;

get_build_shell:
	docker run  -v`pwd`:/home/jop_workspace/ --network=host -w /home/jop_workspace/ -it jop_builder:${JOP_VER} "/bin/bash"





