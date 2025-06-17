#!/bin/bash
cat <<'DIAGRAM'
            +---------------+
            | PumpFun Site  |
            +---------------+
                    |
                [Scraper]
                    |
             +-------------+
             | Data Store  |
             +-------------+
              /           \
Phase 2 --> [Telegram Bot]  \
              \             \
          Phase 3 --> [Web Application]
DIAGRAM
