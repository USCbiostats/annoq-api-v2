new_cron_job="0 0 * * 1 downloads -type f -exec rm {} \;"

(crontab -l 2>/dev/null; echo "$new_cron_job") | crontab -
