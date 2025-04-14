const isProduction = window.location.hostname.includes("saman-moeinsadat-ai-lab.de");

window.CONFIG = {
    BACKEND_URL: isProduction
                ?  "https://keyword-extractor.saman-moeinsadat-ai-lab.de" 
                :  "http://127.0.0.1:8000"
  };