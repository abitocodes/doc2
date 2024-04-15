#!/bin/bash

# _results 디렉터리로 이동
cd _results

# .pdf.pdf로 끝나는 모든 파일을 찾아서 이름을 수정
for file in *.pdf.pdf; do
    # 새 파일명을 기존 파일명에서 마지막의 .pdf를 제거하여 생성
    new_name="${file%.pdf}"
    # 파일 이름 변경
    mv "$file" "$new_name"
    echo "Renamed $file to $new_name"
done
