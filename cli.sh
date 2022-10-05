if [ ! -f "cockroach" ]; then
    curl https://binaries.cockroachdb.com/cockroach-v22.1.6.linux-amd64.tgz | tar -xz
    mv ./cockroach-v22.1.6.linux-amd64/cockroach ./cockroach
fi

./cockroach sql --url $PG_CONN_STRING