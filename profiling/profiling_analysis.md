# **Analysis of Profiling Reports - TVMaze Dataset (January 2024)**

This report summarizes the main findings obtained from exploratory analysis using `ydata_profiling`, based on the data extracted from the TVMaze API dating from January 2024.

---

## **Table: `fact_episodes`**

### **Observations**
- The key columns `episode_id` and `show_id` are complete and do not contain null values.  
- 11.2% of the values for `episode_runtime` are missing. If it's necessary to calculate the average runtime of a show based on its episodes, the metric would be significantly affected.  
- No duplicate rows were detected, which is a positive sign since the desired level of granularity is at the episode level.

---

## **Table: `dim_shows`**

### **Observations**
- The field `show_avg_runtime` is missing for several shows—approximately 8.6% of them. This is explained by the fact that not all shows have this data declared on the website from which the data was extracted.  
- In 11.3% of shows, the `show_official_site` field is missing. This field represents the show's URL. Therefore, we acknowledge there will be a lack of information when selecting the unique domains associated with shows.  
- The columns `show_id` and `show_name` are complete.  
- No duplicate rows were found.

---

## **Table: `dim_genres`**

### **Observations**
- The column `genre_name` contains only one category per row, thanks to the correct use of `.explode()` on the list of genres per show.  
- Some minor inconsistencies were identified, such as extra spaces in genre names.

---

## **Table: `show_genres`**

### **Observations**
- This table represents the many-to-many relationship between shows and genres. This is because one or more genres can be assigned to a show.  
- It does not contain null values or duplicates after the merge with `dim_genres`.

---

## **General Conclusions**

It is necessary to carry out a data conditioning process across the tables, particularly to handle missing or null values. Below are some processing actions to be implemented:

- Any row in the tables that contains null values in key fields such as `episode_id`, `show_id`, or `genre_id` should be removed, as they compromise the referential integrity of the data model.

- In cases where `show_avg_runtime` is null, it will be replaced with the value `0` as a standard strategy, understanding that some shows do not have average runtime data available from the source.

- Duplicate records must be removed from all tables (`fact_episodes`, `dim_shows`, `dim_genres`, `show_genres`) to ensure uniqueness by key fields.

- In the `dim_genres` table, values in the `genre_name` column should be cleaned using `.str.strip()` to remove leading or trailing whitespace, which helps prevent semantic duplicates or errors.
