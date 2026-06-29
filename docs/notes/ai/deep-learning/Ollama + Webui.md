
# Setup
```
services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "127.0.0.1:11434:11434"
    volumes:
      - /Ollama/data:/root/.ollama
    environment:
      - OLLAMA_NUM_PARALLEL=4          # 동시 추론 요청
      - OLLAMA_MAX_LOADED_MODELS=1     # GPU 메모리에 유지할 최대 모델
      - OLLAMA_FLASH_ATTENTION=1
    deploy:
      resources:
        limits:
          memory: 32G
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    tty: true
    networks:
      - Wan
    restart: unless-stopped

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - "3000:8080"
    volumes:
      - /Ollama/backend/data:/app/backend/data
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - WEBUI_SECRET_KEY=${WEBUI_SECRET_KEY}
      - WEBUI_AUTH=true
      - DEFAULT_USER_ROLE=pending
      - ENABLE_SIGNUP=false
      - HF_HUB_DISABLE_SYMLINKS_WARNING=1
      - HF_TOKEN=${HF_TOKEN}
      - ENABLE_WEB_SEARCH=true
      - WEB_SEARCH_ENGINE=searxng
      - SEARXNG_QUERY_URL=http://searxng:8080/search?q=<query>
      - WEB_SEARCH_RESULT_COUNT=5
      - WEB_SEARCH_CONCURRENT_REQUESTS=10
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"
    depends_on:
      - ollama
    networks:
      - Wan
    restart: unless-stopped

  searxng:
    image: docker.io/searxng/searxng:latest
    container_name: searxng
    volumes:
      - ./searxng:/etc/searxng:rw
    environment:
      - BIND_ADDRESS=0.0.0.0:8080
      - SEARXNG_BASE_URL=http://searxng:8080/
      - UWSGI_WORKERS=4
      - UWSGI_THREADS=4
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETGID
      - SETUID
    networks:
      - Wan
    restart: unless-stopped

networks:
  Wan:
    driver: bridge
```