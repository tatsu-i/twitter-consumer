FROM docker.elastic.co/logstash/logstash:8.0.0

USER root
RUN update-ca-certificates
COPY ./logstash.conf /usr/share/logstash/pipeline/logstash.conf
USER logstash
