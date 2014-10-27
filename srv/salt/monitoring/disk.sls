check_/:
  disk.status:
    - name: /
    - url: http://test.internal/{{ grains.id }}/disk.status/
    - thresholds:
      - critical:
          maximum: 20
      - warning:
          maximum: 1
      - ok:
          result: True
