#pragma once

/**
 * @brief Forward declaration of deletion functions 
 * that must be implemented by the using library, 
 * so that the appropriate memory allocation/freeing functions are called.
 * "new"/"malloc"/"free"/"delete" operations on objects/pointers must be done 
 * within a "module" (i.e. a DLL in effect). 
 * If you allocate memory in a DLL and free it in another that is separated 
 * by a C API, you are likely to end up in trouble, so C APIs should 
 * provide memory deallocation entry points. 
 */

/**
 * @brief Delete an array of C 'strings' (array of character arrays)
 * 
 */

void delete_ansi_string_array(char** values, int arrayLength);
void delete_array(double* a);
