import UIKit

@main
final class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        configurationForConnecting connectingSceneSession: UISceneSession,
        options: UIScene.ConnectionOptions
    ) -> UISceneConfiguration {
        let configuration = UISceneConfiguration(
            name: "Default Configuration",
            sessionRole: connectingSceneSession.role
        )
        configuration.delegateClass = SceneDelegate.self
        return configuration
    }
}

final class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?
    private weak var statusLabel: UILabel?

    func scene(
        _ scene: UIScene,
        willConnectTo session: UISceneSession,
        options connectionOptions: UIScene.ConnectionOptions
    ) {
        guard let windowScene = scene as? UIWindowScene else {
            return
        }

        let controller = UIViewController()
        controller.view.backgroundColor = .systemBackground

        let title = UILabel()
        title.text = "Native runtime evidence"
        title.font = .preferredFont(forTextStyle: .title1)
        title.adjustsFontForContentSizeCategory = true
        title.accessibilityIdentifier = "evidence-title"

        let status = UILabel()
        status.text = UIAccessibility.isReduceMotionEnabled
            ? "Reduced Motion enabled"
            : "Reduced Motion disabled"
        status.font = .preferredFont(forTextStyle: .body)
        status.adjustsFontForContentSizeCategory = true
        status.accessibilityIdentifier = "evidence-status"
        statusLabel = status

        let button = UIButton(type: .system)
        button.setTitle("Confirm runtime", for: .normal)
        button.titleLabel?.font = .preferredFont(forTextStyle: .headline)
        button.accessibilityIdentifier = "evidence-action"
        button.heightAnchor.constraint(greaterThanOrEqualToConstant: 44).isActive = true
        button.addAction(UIAction { [weak self] _ in
            _ = self?.confirmRuntimeInteraction()
        }, for: .touchUpInside)

        let stack = UIStackView(arrangedSubviews: [title, status, button])
        stack.axis = .vertical
        stack.spacing = 20
        stack.translatesAutoresizingMaskIntoConstraints = false
        controller.view.addSubview(stack)
        NSLayoutConstraint.activate([
            stack.leadingAnchor.constraint(
                equalTo: controller.view.safeAreaLayoutGuide.leadingAnchor,
                constant: 24
            ),
            stack.trailingAnchor.constraint(
                equalTo: controller.view.safeAreaLayoutGuide.trailingAnchor,
                constant: -24
            ),
            stack.centerYAnchor.constraint(equalTo: controller.view.centerYAnchor),
        ])

        let window = UIWindow(windowScene: windowScene)
        window.rootViewController = controller
        window.makeKeyAndVisible()
        self.window = window
        print("DESIGN_CRAFT_RUNTIME_LAUNCHED")

        if let url = connectionOptions.urlContexts.first?.url {
            _ = handleRuntimeURL(url)
        }
    }

    func scene(_ scene: UIScene, openURLContexts urlContexts: Set<UIOpenURLContext>) {
        guard let url = urlContexts.first?.url else {
            return
        }
        _ = handleRuntimeURL(url)
    }

    private func handleRuntimeURL(_ url: URL) -> Bool {
        print("DESIGN_CRAFT_RUNTIME_URL_RECEIVED:\(url.absoluteString)")
        guard url.scheme == "designcraft-evidence", url.host == "confirm" else {
            return false
        }
        return confirmRuntimeInteraction()
    }

    private func confirmRuntimeInteraction() -> Bool {
        statusLabel?.text = "Runtime interaction confirmed"
        guard let documents = FileManager.default.urls(
            for: .documentDirectory,
            in: .userDomainMask
        ).first else {
            print("DESIGN_CRAFT_RUNTIME_INTERACTION_FAILED:no-documents-directory")
            return false
        }
        do {
            try "Runtime interaction confirmed\n".write(
                to: documents.appendingPathComponent("runtime-interaction.txt"),
                atomically: true,
                encoding: .utf8
            )
            print("DESIGN_CRAFT_RUNTIME_INTERACTION_CONFIRMED")
            return true
        } catch {
            print("DESIGN_CRAFT_RUNTIME_INTERACTION_FAILED:\(error)")
            return false
        }
    }
}
