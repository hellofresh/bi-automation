from kafka import KafkaConsumer
import statsd


if __name__ == '__main__':
    c = statsd.StatsClient('graphite000.tools.hellofresh.io', 8125, prefix='dwh.live.kafka')

    servers = 'kafka-cloudera000.live.bi.hellofresh.io:9092,kafka-cloudera001.live.bi.hellofresh.io:9091'
    topics = ['adjust_android','adjust_ios','adjust_unknown','adyen_reports','at','boxes_shipped_status','boxes_shipped_status_bridged','boxes_shipped_status_dev','boxes_shipped_status_staging','cancellation_survey','cancellation_survey_bridged','cancellation_survey_staging','communication_preferences_service','container','csi_producer_dev','csi_producers_dev','customer','customer_account_deactivated','customer_account_deactivated_dev','customer_account_deactivated_staging','customer_account_reactivated','customer_account_reactivated_dev','customer_account_reactivated_staging','customer_box_shipped','customer_box_shipped_bridged','customer_box_shipped_dev','customer_box_shipped_staging','customer_cancelled','customer_cancelled_dev','customer_cancelled_staging','customer_deactivated','customer_deactivated_staging','customer_dev','customer_email_changed','customer_email_changed_dev','customer_email_changed_staging','customer_reactivated','customer_reactivated_dev','customer_reactivated_staging','customer_receive_email_status_changes','customer_receive_email_status_changes_dev','customer_receive_email_status_changes_staging','customer_status_changed','customer_status_changes','customer_status_changes_staging','dev','experiment_created','experiment_updated','loyalty_bank_customer_points_credited','loyalty_bank_customer_points_debited','loyalty_bank_report_points_credited','loyalty_bank_report_points_debited','mealswap','new-orders','new_customer','new_customer_dev','new_customer_staging','new_subscriptions','new_subscriptions_bridged','new_subscriptions_dev','new_subscriptions_staging','newsletter_opt_out_dev','newsletter_optin','newsletter_optin_dev','newsletter_optin_staging','newsletter_option_staging','newsletter_optout','newsletter_optout_dev','newsletter_optout_staging','nps_scores','nps_scores_staging','recipe.rating','recipes_events_live','rjunior_stress_test','staging','subscription_cancelled','subscription_cancelled_bridged','subscription_changed','subscription_changed_bridged','subscription_changed_dev','subscription_changed_staging','subscription_pause_change','subscription_pause_change_bridged','subscription_pause_change_dev','subscription_pause_change_staging','subscription_reactivated','subscription_status','subscription_status_bridged','subscription_status_staging','subscription_status_test','subscription_status_topic','subscriptions_status','test','test.topic.dot.notation','test_customers_staging_iurii','test_subscription_changed_command','test_topic_iurii','tracking_sessions']

    consumer = KafkaConsumer(
        bootstrap_servers=servers
    )

    consumer.subscribe(topics)

    for msg in consumer:
        topic = msg.topic
        print topic
        c.incr('{}.processed'.format(topic))
