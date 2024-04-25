```mermaid
graph TD;
    prompt_start-->

    Q0001_init_bot-->
    Q0100_send_job_highlight-->
    Q0201_send_candidate_background-->
    background_send_end;

    background_send_end-->
    Q0105_filter_by_candiates_preferences-->
    Q0106_salary_check-->
    preference_check_end;

    preference_check_end--match-->
    Q0300_send_email-->
    Q0301_draft_email-->
    Q0401_review_email

    -->prompt_end;

    preference_check_end--not_match-->stopped_by_preference_check;
```
