window.addEventListener("scroll", revealBlocks);

function revealBlocks() {
  const blocks = document.querySelectorAll(".block");
  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i];
    const blockTop = block.getBoundingClientRect().top;
    const windowHeight = window.innerHeight;
    if (blockTop < windowHeight) {
      block.classList.add("visible");
    }
  }
}
