document.addEventListener("DOMContentLoaded", () => {

    // ---------- MARCAR HÁBITO COMO CUMPLIDO ----------

    const botonesCompletar = document.querySelectorAll(".btn-completar");

    botonesCompletar.forEach((boton) => {
        boton.addEventListener("click", async () => {
            const habitoId = boton.dataset.habitoId;

            // Evitar doble clic mientras se procesa
            if (boton.disabled) return;
            boton.disabled = true;

            try {
                const respuesta = await fetch(`/completar/${habitoId}`, {
                    method: "POST"
                });
                const datos = await respuesta.json();

                const card = boton.closest(".habito-card");
                const rachaNumero = card.querySelector(".racha-numero");
                const rachaLabel = card.querySelector(".racha-label");
                const feedback = card.querySelector(".feedback-positivo");
                const ultimoDia = card.querySelector(".dias-semana .dia-indicador:last-child");

                if (datos.exito) {
                    // Actualizar número de racha
                    rachaNumero.textContent = datos.racha;
                    rachaLabel.textContent = datos.racha === 1 ? "día de racha" : "días de racha";

                    // Marcar el día de hoy (último indicador) como cumplido
                    if (ultimoDia) {
                        ultimoDia.classList.add("dia-cumplido");
                        ultimoDia.classList.remove("dia-pendiente");
                    }

                    // Botón pasa a estado "completado"
                    boton.textContent = "¡Hábito cumplido hoy! ✅";
                    boton.classList.add("completado");

                    // Mostrar animación de feedback
                    feedback.hidden = false;
                    feedback.classList.add("mostrar");

                } else {
                    // Ya estaba marcado hoy
                    boton.textContent = "Ya completado hoy";
                    boton.classList.add("completado");
                }

            } catch (error) {
                console.error("Error al marcar el hábito:", error);
                boton.disabled = false;
            }
        });
    });


    // ---------- ELIMINAR HÁBITO ----------

    const botonesEliminar = document.querySelectorAll(".btn-eliminar");
    const formEliminar = document.getElementById("form-eliminar");

    botonesEliminar.forEach((boton) => {
        boton.addEventListener("click", () => {
            const habitoId = boton.dataset.habitoId;
            const confirmar = confirm("¿Seguro que quieres eliminar este hábito? Se perderá todo su historial.");

            if (confirmar) {
                formEliminar.action = `/eliminar/${habitoId}`;
                formEliminar.submit();
            }
        });
    });

});