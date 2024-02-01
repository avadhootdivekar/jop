SHELL:=/bin/bash 
export SEP:=\n====================================================================================================================================\n
export PROJECT_ROOT:=$(shell pwd)
export JOP_VER:=1.01
export WORKSPACE_DIR:=/home/jop_workspace
export ROBOT_OPTIONS= --outputdir ${WORKSPACE_DIR}/output/test_results 
export BUILD_VER:=1.01
export GO_WORKSPACE_DIR:=/usr/src/app
export WORKSPACE_DIR_HOST:=${PROJECT_ROOT}
export GO_LOG_FILE:=jop.log

all : clean build test generate_bin
	@echo "${SEP} all"

clean:
	@echo "${SEP} Clean"
	cd go/src; 																\
			- rm gen/*;														\
			echo "" > ${GO_LOG_FILE} ;				
	- rm output/test_results/*

build : 
	@echo "${SEP} Build"
	cd antlr/ ; \
		make ; 

tools : 
	@echo "${SEP} tools"

run : 
	@echo -e "${SEP} run" 
	cd antlr/ ; \
		make run; 

test :
	@echo "${SEP} test"
	cd tests/test_cases; \
		robot test-1.robot ;

test_new :
	@echo "${SEP} test"
	cd tests/test_cases; \
		robot --include New  test-1.robot;

build_container :
# Only this recipe runs outside of the container. Rest all will run inside the container. 
# Build  the  container 
	@echo "${SEP} Building build shell."
	docker build -t jop_builder:${JOP_VER} ./ ;

get_build_shell:
	docker run  -v`pwd`:/home/jop_workspace/ --network=host -w /home/jop_workspace/ -it jop_builder:${JOP_VER} "/bin/bash"


build_shell_go:
	@echo "Building Go build shell"
	cd go;																\
			docker build ./ -t jop_go:${BUILD_VER};						\
			docker-compose up -d ;										\
			docker exec -it go_dev-env_1 bash ; 

build_go: mod_tidy
	@echo "Building go"
	cd go/src/;															\
			java -cp ../../artifacts/antlr-4.13.0-complete.jar org.antlr.v4.Tool -Dlanguage=Go  -o gen/  -visitor jop.g4; 		\
			go build;

test_go: mod_tidy
	@echo "Testing go"
	cd go/src/;															\
			go test

mod_tidy:
	cd go/src/;															\
			go mod tidy;					

generate_bin:
	rm -f output/test_1_visitor.bin;
	pushd antlr; python3 -m nuitka --standalone test_1_visitor.py; popd;
	mv antlr/test_1_visitor.bin output/test_1_visitor.bin;

