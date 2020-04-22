files = ["test-1", "test-2", "test-3", "test-4", "test-5"]
rule all:
  input:
    expand("{filename}.txt", filename = files)
    
rule hello_world:
  threads: 4
  resources:
    ntasks=1,
    mem_mb=50
  output:
    "{filename}.txt"
  shell: 
    "echo Hello World > {output}"
