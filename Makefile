
export SEP:=\n====================================================================================================================================\n
export JOP_VER:=1.01
export WORKSPACE_DIR:=/home/jop_workspace
export ROBOT_OPTIONS= --outputdir ${WORKSPACE_DIR}/output/test_results 


all : clean build test
	@echo "${SEP} all"

clean:
	@echo "${SEP} Clean"


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





