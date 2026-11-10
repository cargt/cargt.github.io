/* Image Finder: pick a release, board and image from the nightly builds on
 * yocto.cargt.com and show its files, flashing and update commands, device
 * trees and packages.
 *
 * yocto.cargt.com sends no CORS headers, so this reads a snapshot made by
 * docs/tools/scan_yocto.py when the site is built, not the server itself.
 * Download links still point at yocto.cargt.com.
 */
(function () {
  "use strict";

  var root = document.getElementById("image-finder-app");
  if (!root) return;
  var DATA = root.getAttribute("data-src");
  var index = null;
  var packageCache = {};

  // ---- small DOM helpers ------------------------------------------------

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "text") node.textContent = attrs[k];
        else if (k === "class") node.className = attrs[k];
        else node.setAttribute(k, attrs[k]);
      });
    }
    (children || []).forEach(function (c) {
      if (c == null) return;
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }

  function link(href, text) {
    return el("a", { href: href, text: text || href });
  }

  function code(text) {
    return el("code", { class: "docutils literal notranslate" }, [el("span", { class: "pre", text: text })]);
  }

  // A command block styled like a Sphinx code block, with a copy button.
  function commands(lines) {
    var text = lines.join("\n");
    var btn = el("button", { class: "if-copy", type: "button", title: "Copy", text: "Copy" });
    btn.addEventListener("click", function () {
      navigator.clipboard.writeText(text).then(function () {
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = "Copy"; }, 1500);
      });
    });
    return el("div", { class: "if-code highlight-bash notranslate" }, [
      el("div", { class: "highlight" }, [el("pre", { text: text })]),
      btn,
    ]);
  }

  function section(title, children) {
    return el("div", { class: "if-section" }, [el("h3", { text: title })].concat(children));
  }

  function admonition(kind, title, children) {
    return el("div", { class: "admonition " + kind }, [
      el("p", { class: "admonition-title", text: title }),
    ].concat(children));
  }

  function para(children) {
    return el("p", null, children);
  }

  function doc(page, text, anchor) {
    return link(page + ".html" + (anchor ? "#" + anchor : ""), text);
  }

  function day(date) {
    return (date || "").slice(0, 10);
  }

  // ---- selection ---------------------------------------------------------

  var selRelease = el("select", { id: "if-release", "aria-label": "Release" });
  var selBoard = el("select", { id: "if-board", "aria-label": "Board" });
  var selImage = el("select", { id: "if-image", "aria-label": "Image" });
  var output = el("div", { class: "if-output" });

  function boardLabel(b) {
    var name = b.carrier ? b.som + " / " + b.carrier : b.som;
    return name === b.machine ? b.machine : name + "  (" + b.machine + ")";
  }

  function current() {
    var rel = index.releases[selRelease.selectedIndex];
    var board = rel && rel.boards[selBoard.selectedIndex];
    var image = board && board.images[selImage.selectedIndex];
    return { release: rel, board: board, image: image };
  }

  function fill(select, items, label, wanted) {
    select.innerHTML = "";
    var picked = 0;
    items.forEach(function (item, i) {
      select.appendChild(el("option", { value: String(i), text: label(item) }));
      if (wanted && (item.name === wanted || item.machine === wanted)) picked = i;
    });
    select.selectedIndex = picked;
  }

  function fillBoards(wantedBoard, wantedImage) {
    var rel = index.releases[selRelease.selectedIndex];
    fill(selBoard, rel.boards, boardLabel, wantedBoard);
    fillImages(wantedImage);
  }

  function fillImages(wantedImage) {
    var b = current().board;
    fill(selImage, b ? b.images : [], function (i) { return i.name; }, wantedImage);
    render();
  }

  // ---- output ------------------------------------------------------------

  function render() {
    var c = current();
    output.innerHTML = "";
    if (!c.board || !c.image) {
      output.appendChild(para(["No images found for this release."]));
      return;
    }
    location.replace("#" + [c.release.name, c.board.machine, c.image.name].join("/"));
    output.appendChild(renderBuild(c));
    output.appendChild(renderDownloads(c));
    output.appendChild(renderFlash(c));
    output.appendChild(renderUpdate(c));
    var dt = renderDeviceTrees(c);
    if (dt) output.appendChild(dt);
    output.appendChild(renderPackages(c));
  }

  function renderBuild(c) {
    var info = c.board.build_info || {};
    var rows = [];
    [["Built", info.built], ["Cycle", info.cycle], ["Build ID", info["build-id"]],
     ["Manifest", info.manifest]].forEach(function (r) {
      if (!r[1]) return;
      var value = /^(Built|Cycle)$/.test(r[0]) ? r[1] : code(r[1]);
      rows.push(el("tr", null, [el("th", { text: r[0] }), el("td", null, [value])]));
    });
    var children = [];
    if (rows.length) {
      children.push(el("table", { class: "docutils if-kv" }, [el("tbody", null, rows)]));
    } else {
      children.push(para(["This folder has no ", code("BUILD-INFO.txt"), "."]));
    }

    // Files in one folder are not always from the same nightly.
    var f = c.image.files;
    var disk = f.wic_zst || f.wic_bz2 || f.wic;
    var update = f.swu || c.board.bundles[0];
    var dates = {};
    if (disk) dates[day(disk.date)] = "disk image";
    if (update && !dates[day(update.date)]) dates[day(update.date)] = "update file";
    if (Object.keys(dates).length > 1) {
      children.push(admonition("warning", "Files from different nightlies", [
        para(["The disk image is dated ", code(day(disk.date)), " and the update file ",
              code(day(update.date)), ". Each file is the latest build of that file, and ",
              code("BUILD-INFO.txt"), " describes the most recent build in the folder. ",
              "Check the dates below before you rely on two files matching."]),
      ]));
    }
    return section("Build", children);
  }

  function fileRow(label, file, note) {
    return el("tr", null, [
      el("td", { text: label }),
      el("td", null, [link(file.url, file.name)].concat(note ? [el("br"), el("small", { text: note })] : [])),
      el("td", { class: "if-nowrap", text: file.date }),
      el("td", { class: "if-nowrap", text: file.size }),
    ]);
  }

  function renderDownloads(c) {
    var f = c.image.files;
    var b = c.board;
    var rows = [];
    if (b.bootloader) rows.push(fileRow("Bootloader", b.bootloader));
    if (f.wic_zst) rows.push(fileRow("Disk image", f.wic_zst));
    if (f.wic_bz2) rows.push(fileRow("Disk image (SD card)", f.wic_bz2));
    if (f.bmap) rows.push(fileRow("Block map", f.bmap, "Lets uuu and bmaptool skip empty blocks"));
    if (f.swu) rows.push(fileRow("SWUpdate file", f.swu));
    b.bundles.forEach(function (x) { rows.push(fileRow("RAUC bundle", x)); });
    if (f.sbom) rows.push(fileRow("SBOM (SPDX)", f.sbom));
    if (f.licenses) rows.push(fileRow("Licenses", f.licenses));
    if (f.manifest) rows.push(fileRow("Package list", f.manifest));
    if (b.build_info && b.build_info.file) rows.push(fileRow("Build info", b.build_info.file));

    var table = el("table", { class: "docutils align-default if-files" }, [
      el("thead", null, [el("tr", null, ["File", "Name", "Date", "Size"].map(function (h) {
        return el("th", { class: "head", text: h });
      }))]),
      el("tbody", null, rows),
    ]);
    var children = [el("div", { class: "wy-table-responsive" }, [table]),
      para(["All files: ", link(b.folder)])];
    if (b.family === "stm32mp2") {
      children.push(para(["STM32CubeProgrammer needs the whole folder, not only the files above: ",
        "the flash layout refers to the bootloader, FIP and partition images next to it."]));
    }
    return section("Downloads", children);
  }

  function renderFlash(c) {
    var f = c.image.files;
    var b = c.board;
    var children = [];
    if (b.family === "imx") {
      var boot = b.bootloader ? b.bootloader.name : "imx-boot.tagged";
      var disk = f.wic_zst ? f.wic_zst.name : "<image>.wic.zst";
      if (/^imx95/.test(b.machine)) {
        // As in getting-started and flashing-troubleshooting: the -b scripts
        // do not work on the i.MX 95, and no eMMC procedure is documented.
        children.push(admonition("note", "i.MX 95", [
          para(["On the i.MX 95, ", code("uuu imx-boot"), " and the built-in ", code("-b"),
            " scripts stop after the boot ROM stage. To load the bootloader into RAM over USB, save this as ",
            code("imx95-boot.uuu"), " next to ", code("imx-boot"), " and run ", code("uuu imx95-boot.uuu"), ":"]),
          commands(["uuu_version 1.5.0", "SDPS: boot -f imx-boot", "SDPV: write -f imx-boot -skipspl", "SDPV: jump"]),
          para(["A complete procedure for flashing the eMMC of an i.MX 95 over USB is not documented yet; see ",
            doc("flashing-troubleshooting", "Flashing Troubleshooting", "uuu-imx95"), "."]),
        ]));
      } else {
        children.push(para(["Put the board in USB download mode and check that ", code("uuu -lsusb"),
          " lists it (see ", doc("getting-started", "Getting Started"), "). Then flash the bootloader and image. ",
          "This erases the target storage."]));
        children.push(para([el("strong", { text: "eMMC:" })]));
        children.push(commands(["uuu -bmap -b emmc_all " + boot + " " + disk]));
        children.push(para([el("strong", { text: "SD card:" })]));
        children.push(commands(["uuu -bmap -b sd_all " + boot + " " + disk]));
      }
      children.push(para(["If ", code("uuu"), " waits or fails, see ",
        doc("flashing-troubleshooting", "Flashing Troubleshooting"), "."]));
    } else {
      var layouts = b.flash_layouts.filter(function (l) { return l.image === c.image.name; });
      var emmc = layouts.filter(function (l) { return /FlashLayout_emmc_/.test(l.path); });
      // The plain optee eMMC layout, with no -glt display suffix, is the only
      // one with the A and B partitions that RAUC needs.
      var ab = emmc.filter(function (l) { return !/-glt[0-9a-z]+-optee\.tsv$/.test(l.path); })[0];
      children.push(para([el("strong", { text: "eMMC:" }),
        " download the folder, put the board in USB boot mode, and flash with STM32CubeProgrammer:"]));
      if (ab) {
        children.push(commands(["STM32_Programmer_CLI -c port=usb1 -w " + ab.path]));
        children.push(para(["This is the only eMMC layout with the A and B partitions that RAUC updates need. ",
          "The ", code("-glt…"), " display layouts in the same folder have a single set of partitions. ",
          "See ", doc("rauc-ota-updates", "RAUC A/B Updates"), "."]));
      } else {
        children.push(para(["No eMMC flash layout was found in this folder."]));
      }
      if (f.wic_bz2) {
        children.push(para([el("strong", { text: "SD card:" }), " from a Linux host (check the device with ",
          code("lsblk"), "; everything on the card is erased):"]));
        children.push(commands(["bmaptool copy " + f.wic_bz2.name + " /dev/sdX"]));
      }
      children.push(para(["If the board is not found, see ",
        doc("flashing-troubleshooting", "Flashing Troubleshooting", "stm32cubeprog-troubleshooting"), "."]));
    }
    return section("Flash", children);
  }

  function renderUpdate(c) {
    var f = c.image.files;
    var b = c.board;
    var children = [];
    if (b.family === "imx" && f.swu) {
      children.push(para(["Copy the SWUpdate file to the board (for example to ", code("/data"),
        ") and install it to the other root partition:"]));
      children.push(commands(["scp " + f.swu.name + " root@<board-ip>:/data/",
        "ssh root@<board-ip> swupdate -v -i /data/" + f.swu.name, "ssh root@<board-ip> reboot"]));
      children.push(para(["Or drag it onto the SWUpdate web page at ", code("http://<board-ip>:8080/"), "."]));
      children.push(admonition("note", "No automatic rollback on i.MX", [para([
        "SWUpdate on Cargt i.MX images updates the root file system only and does not roll back by itself. ",
        "See ", doc("software-updates", "Software Updates"), ".",
      ])]));
    } else if (b.bundles.length) {
      var bundle = b.bundles[0].name;
      children.push(para(["On a board flashed with the A/B layout, install the bundle to the inactive bank, then reboot:"]));
      children.push(commands(["scp " + bundle + " root@<board-ip>:/usr/local/",
        "ssh root@<board-ip> rauc install /usr/local/" + bundle, "ssh root@<board-ip> reboot"]));
      children.push(para(["A bank that fails to boot falls back to the previous one. See ",
        doc("rauc-ota-updates", "RAUC A/B Updates"), "."]));
    } else {
      children.push(para(["This folder has no update file for this image."]));
    }
    return section("Update a Running Board", children);
  }

  function renderDeviceTrees(c) {
    var b = c.board;
    if (!b.device_trees.length) return null;
    var imx = b.family === "imx";
    var select = el("select", { "aria-label": "Device tree" });
    // The board's base device tree has the shortest name; start with it.
    var base = b.device_trees.reduce(function (a, n) { return n.length < a.length ? n : a; });
    b.device_trees.forEach(function (n) { select.appendChild(el("option", { value: n, text: n })); });
    select.value = base;
    var out = el("div");
    function show() {
      out.innerHTML = "";
      out.appendChild(commands(["fw_setenv fdtfile " + (imx ? "boot/" : "") + select.value, "reboot"]));
    }
    select.addEventListener("change", show);
    show();
    var children = [
      para(["Each display or camera variant is a separate device tree. To boot a different one, set ",
        code("fdtfile"), " on the board and reboot (see ", doc("displays", "Displays"), "):"]),
      para([select]),
      out,
    ];
    if (imx) {
      children.push(para([code("fdtfile"), " is in the U-Boot environment, outside the A/B root partitions, ",
        "so an update normally leaves it as it is. On the i.MX 93 00363 / 00428 the update changes it once; see ",
        doc("software-updates", "Software Updates"), "."]));
    }
    return section("Device Tree", children);
  }

  function renderPackages(c) {
    var children = [];
    var feeds = c.image.feeds;
    if (feeds.length) {
      children.push(para(["Package feeds for this image, as in its ", code("/etc/apt/sources.list"),
        " (see ", doc("package-management", "Package Management"), "):"]));
      children.push(commands(feeds.map(function (u) { return "deb [trusted=yes] " + u + " ./"; })));
    } else {
      children.push(para(["No package feed is published for this release."]));
    }

    var search = el("input", { type: "search", placeholder: "Search packages", "aria-label": "Search packages" });
    var count = el("p", { class: "if-count" });
    var tbody = el("tbody");
    var table = el("table", { class: "docutils align-default if-packages" }, [
      el("thead", null, [el("tr", null, ["Package", "Architecture", "Version"].map(function (h) {
        return el("th", { class: "head", text: h });
      }))]),
      tbody,
    ]);
    children.push(para([c.image.package_count + " packages in " + c.image.name + "."]));
    children.push(search, count, el("div", { class: "wy-table-responsive" }, [table]));

    var key = c.release.name + "/" + c.board.machine;
    var LIMIT = 200;
    function draw(pkgs) {
      var q = search.value.trim().toLowerCase();
      var hits = q ? pkgs.filter(function (p) { return p[0].toLowerCase().indexOf(q) !== -1; }) : pkgs;
      tbody.innerHTML = "";
      hits.slice(0, LIMIT).forEach(function (p) {
        tbody.appendChild(el("tr", null, [el("td", null, [code(p[0])]), el("td", { text: p[1] }), el("td", { text: p[2] })]));
      });
      count.textContent = hits.length > LIMIT
        ? "Showing " + LIMIT + " of " + hits.length + " matches. Refine the search to see more."
        : hits.length + (hits.length === 1 ? " match." : " matches.");
    }
    function load() {
      if (packageCache[key]) return Promise.resolve(packageCache[key]);
      return fetch(DATA + "/" + key + ".json").then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      }).then(function (d) { packageCache[key] = d; return d; });
    }
    count.textContent = "Loading the package list…";
    load().then(function (d) {
      var pkgs = d[c.image.name] || [];
      draw(pkgs);
      search.addEventListener("input", function () { draw(pkgs); });
    }).catch(function () {
      count.textContent = "The package list could not be loaded. It is also in the Package list file above.";
    });
    return section("Packages", children);
  }

  // ---- start ---------------------------------------------------------------

  function start() {
    var wanted = decodeURIComponent(location.hash.slice(1)).split("/");
    fill(selRelease, index.releases, function (r) { return r.name; }, wanted[0]);
    fillBoards(wanted[1], wanted[2]);
  }

  root.innerHTML = "";
  root.appendChild(el("p", { class: "if-loading", text: "Loading the list of nightly images…" }));
  fetch(DATA + "/index.json").then(function (r) {
    if (!r.ok) throw new Error(r.status);
    return r.json();
  }).then(function (data) {
    index = data;
    root.innerHTML = "";
    var picker = el("div", { class: "if-picker" }, [
      el("label", null, ["Release", selRelease]),
      el("label", null, ["Board", selBoard]),
      el("label", null, ["Image", selImage]),
    ]);
    root.appendChild(picker);
    root.appendChild(el("p", { class: "if-generated" }, [
      "Read from ", link(index.base + "/images/", "yocto.cargt.com"), " on " + index.generated + ".",
    ]));
    root.appendChild(output);
    selRelease.addEventListener("change", function () { fillBoards(); });
    selBoard.addEventListener("change", function () { fillImages(); });
    selImage.addEventListener("change", render);
    start();
  }).catch(function () {
    root.innerHTML = "";
    root.appendChild(admonition("warning", "Image list not available", [para([
      "The list of nightly images could not be loaded. Browse the images directly at ",
      link("https://yocto.cargt.com/images/"), ", or use the table in ", doc("releases", "Releases and Downloads"), ".",
    ])]));
  });
})();
