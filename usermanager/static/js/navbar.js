/*
* BetterNav - Bootstrap Navbar + bigSlide (for mobile)
* ATTENTION: CSS does not use browser prefixes, modify if you decide to use in production!
*/
$(document).ready(function() {
  /* Navbar specifics */
    $('.better-nav').each(function(){
      /* Set max width of fixed navbar equal to parent element (ignore this it's project specific) */
      $parentMaxWidth = $('dummy').css('max-width');
      $('.container', this).css('max-width', $parentMaxWidth);
      /* Add body padding if navbar is fixed on top or bottom */
      if($('.better-nav').hasClass('fixed-top')) {
        var $navHeight = $(this).height();
        $('body').css('padding-top', $navHeight+'px');
      } else if($('.better-nav').hasClass('fixed-bottom')) {
        var $navHeight = $(this).height();
        $('body').css('padding-bottom', $navHeight+'px');
      }
    });
  /* Clone main navbar for mobile */
    $('.better-nav .toggle').on('click touchstart', function(){
      $('#navbar-slide').empty();
      $(this).siblings('.body').clone().appendTo("#navbar-slide");
      betterNavPillsInit('#navbar-slide li.dropdown .selector');
    });
  /* Navbar pills dropdown trigger */
    function betterNavPillsInit($action) {
      $($action).on('click tap', function(){
        if($(this).parent('li.dropdown').hasClass('opened')) {
          $(this).parent('li.dropdown').removeClass('opened');
        } else {
          $(this).parent('li.dropdown').addClass('opened');
        }
      });
    }
    betterNavPillsInit('li.dropdown .selector');
  /* Initialize bigSlide */
    $('.better-nav .toggle').bigSlide({
      'menu': '#navbar-slide',
      'push': 'body',
      'side': 'left',
      'menuWidth':  '80%',
      'speed':  300,
      'easyClose':  true,
      afterOpen: function() {
        $('body').css('overflow', 'hidden');
        $('#underlay').addClass('active');
      },
      afterClose: function() {
        setTimeout(function() {
          $('body').css('overflow', 'visible');
        }, 300);
        $('#underlay').removeClass('active');
      }
    });
    /* Dummy Content */
    var $dummyCount = 0;
    while ($dummyCount < 5 ) {
      $('<article><content><h3>DUMMY ARTICLE</h3></content></article>').appendTo('dummy');
      $dummyCount++;
    }
});

