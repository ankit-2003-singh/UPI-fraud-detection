const API_URL = "http://127.0.0.1:5000/api/stream";

async function fetchStream(){
  const res = await fetch(API_URL);
  return await res.json();
}
