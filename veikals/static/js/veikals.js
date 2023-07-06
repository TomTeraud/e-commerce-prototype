// proceed only when all imgs is loaded
window.addEventListener('load', function() {
    // Initialize masonry here
    jQuery(function($) {
        $('.masonry-grid').masonry({
            itemSelector: '.masonry-item',
            columnWidth: '.masonry-item',
            percentPosition: true,
            gutter: 0, // Adjust the gutter size as needed
            isFitWidth: true // Adjust the column width to fit the container
        });
    });
});

// Initialize Fancybox on elements with the 'fancybox' class when the document is ready
$(function() {
    $('.fancybox').fancybox();
  });
  