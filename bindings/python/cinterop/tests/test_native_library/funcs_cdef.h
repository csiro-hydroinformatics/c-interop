
void set_date(date_time_to_second * start, int year, int month, int day, int hour, int min, int sec);
int get_year(date_time_to_second start);
date_time_to_second * create_date(int year, int month, int day, int hour, int min, int sec);
void dispose_date(date_time_to_second * start);

void set_nvv(named_values_vector * nvv);
named_values_vector * create_nvv();
void dispose_nvv(named_values_vector * nvv);
