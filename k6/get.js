// https://k6.io/docs/using-k6/http-requests/
// https://k6.io/docs/using-k6/metrics/

import { Counter } from 'k6/metrics'
import http from 'k6/http'

const delay = 5 // ms

export const options = {
  vus: 10,
  duration: '30s',
}

const okCounter = new Counter('200 OK')
const abortCounter = new Counter('429 Too Many Requests')

export default function () {
  const res = http.get('http://localhost:8080/?user=1&delay=' + delay)
  if (res.status == 429) {
    abortCounter.add(1)
  } else if (res.status == 200) {
    okCounter.add(1)
  }
}