/* ============================================================
   STUDIO G85 — camada de medição, consentimento e conversão
   Carregado por todas as páginas do site.

   COMO ATIVAR O TRACKING (leva 2 minutos):
   1. GA4     → troque 'G-XXXXXXXXXX' pelo ID de medição da propriedade.
   2. Meta    → troque '000000000000000' pelo ID do pixel.
   Enquanto os IDs forem placeholders nada é carregado — nenhuma
   requisição sai do navegador e nenhum cookie é gravado.
   ============================================================ */
(function (w, d) {
  'use strict';

  var CFG = {
    ga4:   'G-XXXXXXXXXX',       // <- ID de medição do GA4
    pixel: '000000000000000',    // <- ID do Meta Pixel
    consentKey: 'g85:consent:v1'
  };

  var temGA4   = /^G-[A-Z0-9]{6,}$/.test(CFG.ga4);
  var temPixel = /^\d{10,}$/.test(CFG.pixel) && CFG.pixel !== '000000000000000';

  /* ---------- dataLayer: sempre existe, mesmo sem GA4 ---------- */
  w.dataLayer = w.dataLayer || [];
  function gtag() { w.dataLayer.push(arguments); }
  w.gtag = w.gtag || gtag;

  /* ---------- consentimento (LGPD) ----------
     Consent Mode v2: negado por padrão, liberado só após o aceite. */
  function lerConsentimento() {
    try { return localStorage.getItem(CFG.consentKey); } catch (e) { return null; }
  }
  function gravarConsentimento(v) {
    try { localStorage.setItem(CFG.consentKey, v); } catch (e) {}
  }

  gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted',
    wait_for_update: 500
  });

  var consentimento = lerConsentimento();
  if (consentimento === 'aceito') liberarConsentimento();

  function liberarConsentimento() {
    gtag('consent', 'update', {
      ad_storage: 'granted',
      ad_user_data: 'granted',
      ad_personalization: 'granted',
      analytics_storage: 'granted'
    });
    carregarTags();
  }

  /* ---------- carregamento das tags ---------- */
  var tagsCarregadas = false;
  function carregarTags() {
    if (tagsCarregadas) return;
    tagsCarregadas = true;

    if (temGA4) {
      var s = d.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=' + CFG.ga4;
      d.head.appendChild(s);
      gtag('js', new Date());
      gtag('config', CFG.ga4, { send_page_view: true });
    }

    if (temPixel) {
      /* snippet oficial do Meta Pixel */
      !function (f, b, e, v, n, t, s) {
        if (f.fbq) return; n = f.fbq = function () {
          n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
        };
        if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = [];
        t = b.createElement(e); t.async = !0; t.src = v;
        s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
      }(w, d, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
      w.fbq('init', CFG.pixel);
      w.fbq('track', 'PageView');
    }

    /* eventos que ficaram na fila antes do aceite */
    while (fila.length) { var ev = fila.shift(); despachar(ev[0], ev[1]); }
  }

  /* ---------- API de eventos ---------- */
  var fila = [];

  function despachar(nome, params) {
    params = params || {};
    if (temGA4 && w.gtag) w.gtag('event', nome, params);
    if (temPixel && w.fbq) {
      if (nome === 'gerar_lead' || nome === 'clique_whatsapp') {
        w.fbq('track', 'Lead', params);
      } else if (nome === 'contato') {
        w.fbq('track', 'Contact', params);
      } else {
        w.fbq('trackCustom', nome, params);
      }
    }
  }

  /* Evento público: sempre entra no dataLayer (para GTM / depuração);
     só vai para GA4/Meta depois do consentimento. */
  w.g85Evento = function (nome, params) {
    params = params || {};
    w.dataLayer.push(Object.assign({ event: nome }, params));
    if (lerConsentimento() === 'aceito' && tagsCarregadas) despachar(nome, params);
    else if (lerConsentimento() === 'aceito') fila.push([nome, params]);
  };

  /* ---------- cliques em WhatsApp / telefone ----------
     Delegação: pega qualquer link wa.me ou tel:, em qualquer página,
     inclusive os inseridos depois do carregamento. */
  d.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';

    if (href.indexOf('wa.me') > -1 || href.indexOf('api.whatsapp.com') > -1) {
      w.g85Evento('clique_whatsapp', {
        origem: a.getAttribute('data-origem') || contexto(a),
        pagina: d.title,
        caminho: location.pathname
      });
    } else if (href.indexOf('tel:') === 0) {
      w.g85Evento('clique_telefone', { origem: contexto(a), caminho: location.pathname });
    } else if (href.indexOf('instagram.com') > -1) {
      w.g85Evento('clique_instagram', { caminho: location.pathname });
    } else if (href.indexOf('maps.app.goo.gl') > -1 || href.indexOf('google.com/maps') > -1) {
      w.g85Evento('clique_rota', { caminho: location.pathname });
    }
  }, true);

  /* rótulo da seção em que o botão está — dá para separar
     "WhatsApp do hero" de "WhatsApp do rodapé" no relatório */
  function contexto(el) {
    var sec = el.closest ? el.closest('section[id], footer, header') : null;
    if (!sec) return 'indefinido';
    return sec.id || sec.tagName.toLowerCase();
  }

  /* ---------- profundidade de rolagem (engajamento) ---------- */
  var marcos = [25, 50, 75, 100], vistos = {};
  var pendente = false;
  w.addEventListener('scroll', function () {
    if (pendente) return;
    pendente = true;
    requestAnimationFrame(function () {
      pendente = false;
      var h = d.documentElement.scrollHeight - w.innerHeight;
      if (h <= 0) return;
      var pct = Math.round((w.scrollY / h) * 100);
      for (var i = 0; i < marcos.length; i++) {
        var m = marcos[i];
        if (pct >= m && !vistos[m]) {
          vistos[m] = true;
          w.g85Evento('rolagem', { profundidade: m });
        }
      }
    });
  }, { passive: true });

  /* ---------- banner de cookies ---------- */
  function montarBanner() {
    if (lerConsentimento()) return;

    var box = d.createElement('div');
    box.className = 'ck';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-live', 'polite');
    box.setAttribute('aria-label', 'Aviso de cookies');
    box.innerHTML =
      '<div class="ck__txt">' +
        '<b>Este site usa cookies.</b>' +
        '<p>Usamos cookies para medir audiência e entender quais páginas levam a orçamentos. ' +
        'Você escolhe: nada é carregado antes do seu aceite. ' +
        '<a href="' + raiz() + 'politica-de-privacidade.html">Política de privacidade</a>.</p>' +
      '</div>' +
      '<div class="ck__acts">' +
        '<button type="button" class="ck__btn ck__btn--ghost" data-ck="recusar">Recusar</button>' +
        '<button type="button" class="ck__btn" data-ck="aceitar">Aceitar</button>' +
      '</div>';
    d.body.appendChild(box);
    requestAnimationFrame(function () { box.classList.add('on'); });

    box.addEventListener('click', function (e) {
      var b = e.target.closest('[data-ck]');
      if (!b) return;
      var acao = b.getAttribute('data-ck');
      gravarConsentimento(acao === 'aceitar' ? 'aceito' : 'recusado');
      if (acao === 'aceitar') liberarConsentimento();
      box.classList.remove('on');
      setTimeout(function () { box.remove(); }, 420);
    });
  }

  /* caminho até a raiz do site — as páginas de serviço ficam em /servicos/ */
  function raiz() {
    return /\/servicos\//.test(location.pathname) ? '../' : '';
  }
  w.g85Raiz = raiz;

  /* permite reabrir a escolha a partir da política de privacidade */
  w.g85RevisarCookies = function () {
    try { localStorage.removeItem(CFG.consentKey); } catch (e) {}
    location.reload();
  };

  /* ---------- formulário de lead ---------- */
  var WA = '558598484104';

  function ligarFormulario() {
    var form = d.getElementById('leadForm');
    if (!form) return;
    var status = d.getElementById('leadStatus');

    /* um evento quando a pessoa começa a preencher — mede abandono */
    var iniciou = false;
    form.addEventListener('input', function () {
      if (iniciou) return;
      iniciou = true;
      w.g85Evento('form_iniciado', { formulario: 'orcamento' });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var dados = {
        nome:     form.nome.value.trim(),
        telefone: form.telefone.value.trim(),
        veiculo:  form.veiculo.value.trim(),
        servico:  form.servico.value,
        mensagem: form.mensagem.value.trim()
      };

      if (!dados.nome || dados.nome.length < 2) return invalido(form.nome, 'Escreva seu nome.');
      if (dados.telefone.replace(/\D/g, '').length < 10) {
        return invalido(form.telefone, 'Informe um WhatsApp com DDD.');
      }
      if (!dados.servico) return invalido(form.servico, 'Escolha o serviço.');

      var texto =
        'Olá, Studio G85! Vim pelo site e quero um orçamento.\n\n' +
        'Nome: ' + dados.nome + '\n' +
        'WhatsApp: ' + dados.telefone + '\n' +
        'Veículo: ' + (dados.veiculo || 'não informado') + '\n' +
        'Serviço: ' + dados.servico +
        (dados.mensagem ? '\n\nObservações: ' + dados.mensagem : '');

      w.g85Evento('gerar_lead', {
        formulario: 'orcamento',
        servico: dados.servico,
        caminho: location.pathname
      });

      /* guarda o último lead no próprio navegador: se o WhatsApp não abrir,
         a pessoa não perde o que digitou */
      try { sessionStorage.setItem('g85:ultimo-lead', JSON.stringify(dados)); } catch (err) {}

      if (status) {
        status.textContent = 'Abrindo o WhatsApp com seus dados… se não abrir, chame em (85) 9848-4104.';
        status.className = 'lead__status ok';
      }

      w.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(texto), '_blank', 'noopener');
      form.reset();
    });

    function invalido(campo, msg) {
      if (status) { status.textContent = msg; status.className = 'lead__status erro'; }
      campo.focus();
      campo.setAttribute('aria-invalid', 'true');
      campo.addEventListener('input', function limpar() {
        campo.removeAttribute('aria-invalid');
        campo.removeEventListener('input', limpar);
      });
      return false;
    }

    /* máscara leve de telefone — não atrapalha colar nem apagar */
    var tel = form.telefone;
    tel.addEventListener('input', function () {
      var n = tel.value.replace(/\D/g, '').slice(0, 11);
      if (n.length > 6) tel.value = '(' + n.slice(0, 2) + ') ' + n.slice(2, n.length - 4) + '-' + n.slice(-4);
      else if (n.length > 2) tel.value = '(' + n.slice(0, 2) + ') ' + n.slice(2);
      else tel.value = n;
    });
  }

  /* ---------- vídeos: carregamento sob demanda ----------
     Qualquer <video data-lazy> só baixa quando chega perto da tela. */
  function ligarVideosPreguicosos() {
    var videos = [].slice.call(d.querySelectorAll('video[data-lazy]'));
    if (!videos.length) return;

    if (!('IntersectionObserver' in w)) { videos.forEach(carregar); return; }

    var vio = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (!en.isIntersecting) return;
        carregar(en.target);
        vio.unobserve(en.target);
      });
    }, { rootMargin: '300px 0px' });

    videos.forEach(function (v) { vio.observe(v); });

    function carregar(v) {
      var fontes = [].slice.call(v.querySelectorAll('source[data-src]'));
      if (!fontes.length) return;
      fontes.forEach(function (s) {
        s.src = s.getAttribute('data-src');
        s.removeAttribute('data-src');
      });
      v.load();
      v.removeAttribute('data-lazy');
    }
  }

  function iniciar() {
    montarBanner();
    ligarFormulario();
    ligarVideosPreguicosos();
  }

  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})(window, document);
