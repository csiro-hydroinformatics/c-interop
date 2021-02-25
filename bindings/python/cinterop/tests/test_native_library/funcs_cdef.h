
void delete_char_array(char* ptr);

void set_date(date_time_to_second * start, int year, int month, int day, int hour, int min, int sec);
int get_year(date_time_to_second start);
date_time_to_second * create_date(int year, int month, int day, int hour, int min, int sec);
void dispose_date(date_time_to_second * start);

void set_nvv(named_values_vector * nvv);
named_values_vector * create_nvv();
void dispose_nvv(named_values_vector * nvv);
double first_in_nvv(named_values_vector nvv);

void set_vv(values_vector* vv);
values_vector* create_vv();
void dispose_vv(values_vector* vv);
double first_in_vv(values_vector vv);

// //   66,1: typedef struct _character_vector
void set_cvec(character_vector* cvec);
character_vector* create_cvec();
void dispose_cvec(character_vector* cvec);
char* first_in_cvec(character_vector cvec);

// //   78,1: typedef struct _string_string_map
void set_ssm(string_string_map* ssm);
string_string_map* create_ssm();
void dispose_ssm(string_string_map* ssm);
char* value_for_key_ssm(const char* key, string_string_map ssm);

void set_tsg(regular_time_series_geometry * tsg);
regular_time_series_geometry * create_tsg();
void dispose_tsg(regular_time_series_geometry * tsg);
int tscode_tsg(regular_time_series_geometry tsg);

multi_regular_time_series_data* create_mtsd();
void dispose_mtsd(multi_regular_time_series_data* mtsd);
