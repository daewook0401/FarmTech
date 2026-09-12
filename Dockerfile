# syntax=docker/dockerfile:1
ARG JAVA_IMAGE=eclipse-temurin:17-jre-jammy@sha256:ec72ba5962b45ae4e7f96bfb5ebf6eeb34a488b967f937c8e14f0aaec688954f

FROM ${JAVA_IMAGE} AS forge
COPY tools/download.sh /build/download.sh
COPY pack/forge.tsv /build/forge.tsv
RUN bash /build/download.sh /build/forge.tsv /build/downloads
WORKDIR /opt/farmtech
RUN java -jar /build/downloads/forge-installer.jar --installServer . > /tmp/forge-install.log 2>&1 \
    || { cat /tmp/forge-install.log; exit 1; }

FROM ${JAVA_IMAGE} AS mods
COPY tools/download.sh /build/download.sh
COPY pack/mods.tsv /build/mods.tsv
RUN bash /build/download.sh /build/mods.tsv /build/downloads

FROM ${JAVA_IMAGE} AS runtime
COPY --from=forge /opt/farmtech/libraries /opt/farmtech/libraries
COPY --from=mods /build/downloads/mods /opt/farmtech/mods
COPY pack/defaults /opt/farmtech/defaults
COPY pack/manifest.json /opt/farmtech/manifest.json
COPY --chmod=755 scripts/entrypoint.sh /opt/farmtech/entrypoint.sh
WORKDIR /data
USER 1000:1000
EXPOSE 25565/tcp
ENTRYPOINT ["bash", "/opt/farmtech/entrypoint.sh"]
