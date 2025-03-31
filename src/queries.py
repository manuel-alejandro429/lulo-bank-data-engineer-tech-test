
# File dedicated to develop the queries to execute into our SQLite Data Base


query_avg_runtime_show  = """
    SELECT
        show_id,
        show_name,
        show_avg_runtime average_runtime
    FROM dim_shows
"""

query_shows_by_genre = """
    SELECT 
        g.genre_name,
        COUNT(DISTINCT s.show_id) AS total_shows
    FROM show_genres s
    JOIN dim_genres g 
    ON 
        s.genre_id = g.genre_id
    GROUP BY g.genre_name
    ORDER BY total_shows DESC
"""


query_unique_show_domains= """
    WITH 
    show_domains AS (   -- Here I Select the domains to then keep the distinct ones
        SELECT 
            show_id,
            show_name,
            SUBSTR(
                show_official_site,
                INSTR(show_official_site, '//') + 2,
                INSTR(SUBSTR(show_official_site, INSTR(show_official_site, '//') + 2), '/') - 1
            ) AS domain
        FROM dim_shows
        WHERE show_official_site IS NOT NULL
    )
    SELECT 
        DISTINCT domain
    FROM 
        show_domains
    WHERE domain IS NOT NULL
"""
