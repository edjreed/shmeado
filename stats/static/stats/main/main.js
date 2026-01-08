// Fetch API
async function urlToJson(url) {
  try {
    let response = await fetch(url);
    if (!response.ok) {
      throw new Error(response.status);
    }
    let api = await response.json();
    return api;
  } catch (error) {
    console.error("Error fetching URL:", error);
    return { error: error.message };
  }
}
