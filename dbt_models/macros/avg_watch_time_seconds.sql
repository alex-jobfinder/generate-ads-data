{% macro avg_watch_time_seconds(video_start, video_q25, video_q50, video_q75, video_q100, asset_seconds=30.0) %}
    CASE 
        WHEN {{ video_start }} <= 0 THEN 0.0
        ELSE (
            -- Segment 0: 0-25% (0 to q25)
            GREATEST(0, {{ video_start }} - {{ video_q25 }}) * ({{ asset_seconds }} * 0.125) +
            -- Segment 1: 25-50% (q25 to q50)  
            GREATEST(0, {{ video_q25 }} - {{ video_q50 }}) * ({{ asset_seconds }} * 0.375) +
            -- Segment 2: 50-75% (q50 to q75)
            GREATEST(0, {{ video_q50 }} - {{ video_q75 }}) * ({{ asset_seconds }} * 0.625) +
            -- Segment 3: 75-100% (q75 to q100)
            GREATEST(0, {{ video_q75 }} - {{ video_q100 }}) * ({{ asset_seconds }} * 0.875) +
            -- Segment 4: 100% (q100)
            GREATEST(0, {{ video_q100 }}) * ({{ asset_seconds }} * 1.0)
        ) / CAST({{ video_start }} AS FLOAT)
    END
{% endmacro %}
