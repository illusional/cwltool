class: CommandLineTool
cwlVersion: v1.1
requirements:
  DockerRequirement:
    dockerPull: debian:stretch-slim
    dockerOutputDirectory: /other
inputs: []
outputs:
  thing:
    type: File
    outputBinding:
      glob: thing
baseCommand: ["touch", "/other/thing"]
