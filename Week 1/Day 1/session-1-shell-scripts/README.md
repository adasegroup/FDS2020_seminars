
# Outline of Part 1:
  * Understand the task: input/output is a set of pointclouds in HDF5, but the program isn’t accepting this kind of data exactly, so needs to convert data using an external procedure

## Step 1.
  * Create a bash script and test it running doing nothing
  * Add launching voronoi into the bash script, Add splitting/joining data into the bash script, test so it works

## Step 2.
  * Substitute data that we must process for variables in bash
  * Explain: variable concatenation, curly braces, linebreaks

## Step 3.
  * Variable expansions — make input and output filenames coincide
  * Loops: for, while, find -exec
  * https://stackoverflow.com/questions/9612090/how-to-loop-through-file-names-returned-by-find 

## Step 4.
  * Parse arguments from command-line
  * Functions (usage)
  * Case clause 
  * Test existence of files 
  * If-else clause 

## Step 5. 
  * Make temporary directories
  * Compute nicer absolute filenames from relative 
  * Use GNU parallel to speed things up
