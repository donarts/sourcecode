import requests
import os
import pyrfc6266
import urllib.parse


# url 은 get 방식으로 다운로드 하기 위한 주소가 됩니다.
# path 는 다운로드 경로가 됩니다.
# 성공시 Full path 파일 이름이 넘어옵니다.
def download_get(url, dest_folder="."):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist
    r = requests.get(url, stream=True)
    filename = pyrfc6266.requests_response_to_filename(r)
    print(r.headers, filename)
    if filename == "" or filename is None:
        filename = url.split('/')[-1].replace(" ", "_")
    elif '%' in filename:
        filename = urllib.parse.unquote(filename)

    file_path = os.path.join(dest_folder, filename)

    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 512):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))
        return None
    return file_path

if __name__ == "__main__":
    url = 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png'
    print(download_get(url, "."))
    url = 'https://cdn.hancom.com/link/docs/%ED%95%9C%EA%B8%80%EB%AC%B8%EC%84%9C%ED%8C%8C%EC%9D%BC%ED%98%95%EC%8B%9D3.0_HWPML_revision1.2.hwp'
    print(download_get(url, "."))

# Result ####################
#{'Accept-Ranges': 'bytes', 'Content-Type': 'image/png', 'Cross-Origin-Resource-Policy': 'cross-origin', 'Cross-Origin-Opener-Policy-Report-Only': 'same-origin; report-to="static-on-bigtable"', 'Report-To': '{"group":"static-on-bigtable","max_age":2592000,"endpoints":[{"url":"https://csp.withgoogle.com/csp/report-to/static-on-bigtable"}]}', 'Content-Length': '5969', 'Date': 'Sun, 02 Apr 2023 10:07:31 GMT', 'Expires': 'Sun, 02 Apr 2023 10:07:31 GMT', 'Cache-Control': 'private, max-age=31536000', 'Last-Modified': 'Tue, 22 Oct 2019 18:30:00 GMT', 'X-Content-Type-Options': 'nosniff', 'Server': 'sffe', 'X-XSS-Protection': '0', 'Alt-Svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000'} googlelogo_color_272x92dp.png
#saving to C:\Users\jun\Documents\GitHub\sourcecode\python\example\_52_requests\googlelogo_color_272x92dp.png
#.\googlelogo_color_272x92dp.png
#{'Content-Type': 'application/octet-stream', 'Accept-Ranges': 'bytes', 'X-Agile-Brick-Id': '480527996', 'X-Agile-Checksum': '1121cdabe5929d7aa68704d0516488852bcdc78b4f4b368ad054e8c121d04023', 'X-Agile-Request-Id': '5aaf564a732da062c1c10bf592122357, 24385af8bc6afbe50e767494734b7cfb', 'X-Agile-Source': '111.119.25.183:1987', 'Server': 'CloudStorage', 'Age': '188002', 'Date': 'Sun, 02 Apr 2023 10:07:32 GMT', 'Last-Modified': 'Mon, 10 Nov 2014 01:08:00 GMT', 'X-LLID': '524b2b419aadef6e7827af6fb89c006a', 'Content-Length': '1310720', 'Access-Control-Allow-Origin': '*'} %ED%95%9C%EA%B8%80%EB%AC%B8%EC%84%9C%ED%8C%8C%EC%9D%BC%ED%98%95%EC%8B%9D3.0_HWPML_revision1.2.hwp
#saving to C:\Users\jun\Documents\GitHub\sourcecode\python\example\_52_requests\한글문서파일형식3.0_HWPML_revision1.2.hwp
#.\한글문서파일형식3.0_HWPML_revision1.2.hwp