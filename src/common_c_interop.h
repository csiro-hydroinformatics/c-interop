#pragma once

#ifndef STRDUP
#ifdef _WIN32
#define STRDUP _strdup
#else
#define STRDUP strdup
#endif
#endif // !STRDUP
