/* ═══════════════════════════════════════════════════════════════════════
   app.js — Bordados Personalizados
   ─ Carga catálogo desde la API
   ─ Manejo de carrito en memoria
   ─ Login / Registro contra CSV vía API
   ─ Checkout real con Stripe
   ═══════════════════════════════════════════════════════════════════════ */

// ── Estado global ─────────────────────────────────────────────────────────
const state = {
  productos: [],
  cart: [],
  user: null,
  stripe: null,
  cardElement: null,
  filter: "all",
};

// ── Emojis por categoría ──────────────────────────────────────────────────
const categoryEmoji = { bordado: "🌸", camiseta: "👕", default: "🧵" };

// ═══════════════════════════════════════════════════════════════════════════
//  INIT
// ═══════════════════════════════════════════════════════════════════════════
document.addEventListener("DOMContentLoaded", async () => {
  await loadProductos();
  await initStripe();
  setupForms();
});

// ═══════════════════════════════════════════════════════════════════════════
//  STRIPE INIT
// ═══════════════════════════════════════════════════════════════════════════
async function initStripe() {
  try {
    const res  = await fetch("/pago/config");
    const data = await res.json();

    if (!data.publishable_key) {
      console.warn("Stripe publishable key no configurada. El pago no funcionará.");
      return;
    }

    state.stripe = Stripe(data.publishable_key);
    const elements = state.stripe.elements();

    state.cardElement = elements.create("card", {
      style: {
        base: {
          fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
          fontSize: "15px",
          color: "#2c1810",
          "::placeholder": { color: "#c9956c" },
        },
        invalid: { color: "#e53e3e" },
      },
    });

    state.cardElement.mount("#stripe-card-element");

    state.cardElement.on("change", (e) => {
      const errEl = document.getElementById("card-error");
      if (e.error) {
        errEl.textContent = e.error.message;
        errEl.classList.remove("hidden");
      } else {
        errEl.classList.add("hidden");
      }
    });
  } catch (err) {
    console.error("Error iniciando Stripe:", err);
  }
}

// ═══════════════════════════════════════════════════════════════════════════
//  CATÁLOGO
// ═══════════════════════════════════════════════════════════════════════════
async function loadProductos() {
  try {
    const res  = await fetch("/producto");
    const data = await res.json();
    state.productos = data;
    renderProductos(data);
  } catch {
    showToast("No se pudo cargar el catálogo", "error");
  }
}

function renderProductos(lista) {
  const grid  = document.getElementById("productos-grid");
  const empty = document.getElementById("catalogo-empty");

  const filtered = state.filter === "all"
    ? lista
    : lista.filter((p) => p.categoria === state.filter);

  grid.innerHTML = "";

  if (filtered.length === 0) {
    empty.classList.remove("hidden");
    return;
  }
  empty.classList.add("hidden");

  filtered.forEach((p) => {
    const emoji = categoryEmoji[p.categoria] || categoryEmoji.default;
    const card  = document.createElement("div");
    card.className = "product-card";
    card.innerHTML = `
      <div class="card-image">${emoji}</div>
      <div class="card-body">
        <span class="card-category">${p.categoria || "general"}</span>
        <div class="card-name">${p.nombre || "Sin nombre"}</div>
        <div class="card-desc">${p.descripcion || ""}</div>
        <div class="card-footer">
          <span class="card-price">$${parseFloat(p.precio || 0).toFixed(2)}</span>
          <span class="card-stock">${p.stock ? `Stock: ${p.stock}` : ""}</span>
        </div>
        <button class="btn-add" onclick='addToCart(${JSON.stringify(p)})'>
          + Agregar al carrito
        </button>
      </div>`;
    grid.appendChild(card);
  });
}

// Filter buttons
document.querySelectorAll(".filter-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".filter-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    state.filter = btn.dataset.filter;
    renderProductos(state.productos);
  });
});

// ═══════════════════════════════════════════════════════════════════════════
//  CARRITO
// ═══════════════════════════════════════════════════════════════════════════
function addToCart(producto) {
  const exists = state.cart.find((i) => i.id === producto.id);
  if (exists) {
    exists.qty++;
  } else {
    state.cart.push({ ...producto, qty: 1 });
  }
  renderCart();
  showToast(`"${producto.nombre}" agregado al carrito ✓`, "success");
}

function removeFromCart(id) {
  state.cart = state.cart.filter((i) => i.id !== id);
  renderCart();
}

function renderCart() {
  const count   = state.cart.reduce((s, i) => s + i.qty, 0);
  const total   = state.cart.reduce((s, i) => s + parseFloat(i.precio || 0) * i.qty, 0);
  const badge   = document.getElementById("cart-count");
  const itemsEl = document.getElementById("cart-items");
  const totalEl = document.getElementById("cart-total");

  badge.textContent = count;
  count > 0 ? badge.classList.remove("hidden") : badge.classList.add("hidden");
  totalEl.textContent = `$${total.toFixed(2)}`;

  if (state.cart.length === 0) {
    itemsEl.innerHTML = '<p class="empty-cart">Tu carrito está vacío</p>';
    return;
  }
  itemsEl.innerHTML = state.cart
    .map(
      (i) => `
    <div class="cart-item">
      <div class="cart-item-info">
        <div class="cart-item-name">${i.nombre} ×${i.qty}</div>
        <div class="cart-item-price">$${(parseFloat(i.precio || 0) * i.qty).toFixed(2)}</div>
      </div>
      <button class="btn-remove" onclick="removeFromCart('${i.id}')">🗑</button>
    </div>`
    )
    .join("");
}

document.getElementById("btn-cart").addEventListener("click", () => {
  const drawer = document.getElementById("cart-drawer");
  const overlay = document.getElementById("overlay");
  drawer.classList.toggle("open");
  drawer.classList.toggle("hidden", !drawer.classList.contains("open"));
  overlay.classList.toggle("hidden", !drawer.classList.contains("open"));
});

function closeCart() {
  document.getElementById("cart-drawer").classList.remove("open");
  document.getElementById("cart-drawer").classList.add("hidden");
  document.getElementById("overlay").classList.add("hidden");
}

// ═══════════════════════════════════════════════════════════════════════════
//  CHECKOUT
// ═══════════════════════════════════════════════════════════════════════════
function abrirCheckout() {
  if (state.cart.length === 0) {
    showToast("Tu carrito está vacío", "error");
    return;
  }
  closeCart();

  const total = state.cart.reduce((s, i) => s + parseFloat(i.precio || 0) * i.qty, 0);
  const items = document.getElementById("checkout-items");
  const totalEl = document.getElementById("checkout-total-val");
  const btnMonto = document.getElementById("btn-pagar-monto");

  items.innerHTML = state.cart
    .map(
      (i) => `
    <div class="checkout-item">
      <span>${i.nombre} ×${i.qty}</span>
      <strong>$${(parseFloat(i.precio || 0) * i.qty).toFixed(2)}</strong>
    </div>`
    )
    .join("");

  totalEl.textContent = `$${total.toFixed(2)}`;
  btnMonto.textContent = `$${total.toFixed(2)}`;

  openModal("modal-checkout");
}

async function procesarPago() {
  if (!state.stripe || !state.cardElement) {
    showToast("Stripe no está configurado en el servidor", "error");
    return;
  }

  const nombre = document.getElementById("card-name").value.trim();
  if (!nombre) {
    showToast("Ingresa el nombre de la tarjeta", "error");
    return;
  }

  const total = state.cart.reduce((s, i) => s + parseFloat(i.precio || 0) * i.qty, 0);
  const btnPagar = document.getElementById("btn-pagar");
  btnPagar.disabled = true;
  btnPagar.textContent = "Procesando...";

  try {
    // 1. Crear PaymentIntent en el backend
    const intentRes = await fetch("/pago/crear-intent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        monto: total,
        descripcion: `Pedido Bordados — ${state.user?.email || "cliente"}`,
      }),
    });

    if (!intentRes.ok) {
      const err = await intentRes.json();
      throw new Error(err.detail || "Error al crear el cobro");
    }

    const { client_secret } = await intentRes.json();

    // 2. Confirmar pago con Stripe.js (cobro real)
    const { paymentIntent, error } = await state.stripe.confirmCardPayment(client_secret, {
      payment_method: {
        card: state.cardElement,
        billing_details: {
          name: nombre,
          email: state.user?.email || undefined,
        },
      },
    });

    if (error) throw new Error(error.message);

    if (paymentIntent.status === "succeeded") {
      // 3. Registrar pedido en CSV
      for (const item of state.cart) {
        await fetch("/pedido", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            usuario_email: state.user?.email || "",
            producto_id: parseInt(item.id) || null,
            descripcion: `Compra de ${item.nombre}`,
            talla: null,
            color: null,
            precio_estimado: parseFloat(item.precio) * item.qty,
            estado: "pagado",
          }),
        });
      }

      state.cart = [];
      renderCart();
      closeModal("modal-checkout");
      showToast("¡Pago exitoso! Tu pedido fue registrado 🎉", "success");
    }
  } catch (err) {
    showToast(err.message || "Error en el pago", "error");
    document.getElementById("card-error").textContent = err.message;
    document.getElementById("card-error").classList.remove("hidden");
  } finally {
    btnPagar.disabled = false;
    btnPagar.innerHTML = `Pagar <span id="btn-pagar-monto">$${total.toFixed(2)}</span>`;
  }
}

// ═══════════════════════════════════════════════════════════════════════════
//  FORMULARIOS
// ═══════════════════════════════════════════════════════════════════════════
function setupForms() {
  // Auth button
  document.getElementById("btn-auth").addEventListener("click", () => {
    if (state.user) {
      state.user = null;
      document.getElementById("btn-auth").textContent = "Iniciar sesión";
      showToast("Sesión cerrada", "success");
    } else {
      openModal("modal-auth");
    }
  });

  // Login
  document.getElementById("form-login").addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("l-email").value.trim();
    const pass  = document.getElementById("l-pass").value;
    try {
      const res   = await fetch("/usuario");
      const users = await res.json();
      const found = users.find((u) => u.email === email && u.contrasena === pass);
      if (!found) throw new Error("Correo o contraseña incorrectos");
      state.user = found;
      document.getElementById("btn-auth").textContent = `👤 ${found.nombre_real || found.email}`;
      closeModal("modal-auth");
      showToast(`Bienvenido, ${found.nombre_real || email} 👋`, "success");
    } catch (err) {
      showToast(err.message, "error");
    }
  });

  // Register
  document.getElementById("form-register").addEventListener("submit", async (e) => {
    e.preventDefault();
    const body = {
      nombre_real:     document.getElementById("r-nombre").value.trim(),
      email:           document.getElementById("r-email").value.trim(),
      direccion_envio: document.getElementById("r-dir").value.trim(),
      contrasena:      document.getElementById("r-pass").value,
    };
    try {
      const res = await fetch("/usuario", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error("No se pudo crear la cuenta");
      const created = await res.json();
      state.user = created;
      document.getElementById("btn-auth").textContent = `👤 ${body.nombre_real || body.email}`;
      closeModal("modal-auth");
      showToast("¡Cuenta creada exitosamente! 🎉", "success");
    } catch (err) {
      showToast(err.message, "error");
    }
  });

  // Pedido personalizado
  document.getElementById("form-pedido").addEventListener("submit", async (e) => {
    e.preventDefault();
    const body = {
      usuario_email:   document.getElementById("p-email").value.trim(),
      producto_id:     null,
      descripcion:     document.getElementById("p-descripcion").value.trim(),
      talla:           document.getElementById("p-talla").value || null,
      color:           document.getElementById("p-color").value.trim() || null,
      precio_estimado: parseFloat(document.getElementById("p-precio").value) || null,
      estado:          "pendiente",
    };
    if (!body.usuario_email || !body.descripcion) {
      showToast("Correo y descripción son obligatorios", "error");
      return;
    }
    try {
      const res = await fetch("/pedido", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error("No se pudo enviar el pedido");
      e.target.reset();
      showToast("¡Solicitud enviada! Te contactamos pronto 🧵", "success");
    } catch (err) {
      showToast(err.message, "error");
    }
  });
}

// ═══════════════════════════════════════════════════════════════════════════
//  MODAL helpers
// ═══════════════════════════════════════════════════════════════════════════
function openModal(id) {
  document.getElementById(id).classList.remove("hidden");
  document.getElementById("overlay").classList.remove("hidden");
}
function closeModal(id) {
  document.getElementById(id).classList.add("hidden");
  document.getElementById("overlay").classList.add("hidden");
}
function closeAll() {
  ["modal-auth", "modal-checkout"].forEach(closeModal);
  closeCart();
}
function switchTab(tab) {
  const isLogin = tab === "login";
  document.getElementById("form-login").classList.toggle("hidden", !isLogin);
  document.getElementById("form-register").classList.toggle("hidden", isLogin);
  document.getElementById("tab-login").classList.toggle("active", isLogin);
  document.getElementById("tab-register").classList.toggle("active", !isLogin);
}

// ═══════════════════════════════════════════════════════════════════════════
//  TOAST
// ═══════════════════════════════════════════════════════════════════════════
let toastTimer;
function showToast(msg, type = "default") {
  const toast = document.getElementById("toast");
  toast.textContent = msg;
  toast.className = `toast ${type}`;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.add("hidden"), 3500);
}
