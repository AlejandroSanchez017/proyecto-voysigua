export const tienePermiso = (permiso) => {
  const permisos = JSON.parse(localStorage.getItem("user_permissions") || "[]");
  return permisos.includes(permiso);
};