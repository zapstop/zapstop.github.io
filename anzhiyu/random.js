var posts=["posts/4a17b156.html","posts/a1fb3e72.html"];function toRandomPost(){
    pjax.loadUrl('/'+posts[Math.floor(Math.random() * posts.length)]);
  };