FROM postgres:13.9

#COPY docker/postgres/init.sql /docker-entrypoint-initdb.d/

RUN mkdir /static_files  && cd static_files && mkdir postgres

COPY api_search/scripts/postgres /usr/local/bin/temp
RUN chmod +x /usr/local/bin/temp/* && \
    mv /usr/local/bin/temp/* /usr/local/bin &&  \
    rmdir /usr/local/bin/temp