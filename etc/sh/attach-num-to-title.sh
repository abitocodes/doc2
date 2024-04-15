#!/bin/bash

# _results 디렉터리로 이동
cd _results

# crawled-links-title-2.json 파일을 파싱하여 파일명과 인덱스 매핑 정보를 생성
jq -r '.[] | select(.uppercase_transformed != "") | .uppercase_transformed + ".pdf"' ../crawled-links-title-2.json > mapped_files.txt

# _results 폴더의 모든 PDF 파일을 확인
for file in *.pdf; do
    # mapped_files.txt 파일에서 파일명과 일치하는 줄의 번호를 찾음
    index=$(grep -n "$file" mapped_files.txt | cut -d ':' -f 1)
    if [ -n "$index" ]; then
        # 파일 이름 앞에 인덱스와 하이픈을 추가하여 새 파일명 생성
        new_name="${index}-${file}"
        mv "$file" "$new_name"
        echo "Renamed $file to $new_name"
    else
        echo "No index found for $file in crawled-links-title-2.json"
    fi
done

# 임시 파일 삭제
rm mapped_files.txt
